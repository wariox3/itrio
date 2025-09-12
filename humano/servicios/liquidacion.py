from general.models.configuracion import GenConfiguracion
from humano.models.liquidacion import HumLiquidacion
from humano.models.liquidacion_adicional import HumLiquidacionAdicional
from utilidades.utilidades import Utilidades
from utilidades.backblaze import Backblaze
from datetime import timedelta


class LiquidacionServicio():

    @staticmethod
    def liquidar(liquidacion: HumLiquidacion):  
        adicionales = HumLiquidacionAdicional.objects.filter(liquidacion_id=liquidacion.pk)
        total_adiciones = 0
        total_deducciones = 0

        for adicional in adicionales:
            total_adiciones += adicional.adicional
            total_deducciones += adicional.deduccion

        configuracion = GenConfiguracion.objects.filter(pk=1).values('hum_factor', 'hum_salario_minimo', 'hum_auxilio_transporte')[0]
        auxilio_trasnporte = configuracion['hum_auxilio_transporte']
        fecha_desde = liquidacion.contrato.fecha_desde
        fecha_hasta = liquidacion.contrato.fecha_hasta
        fecha_ultimo_pago_cesantia = fecha_desde
        fecha_ultimo_pago_prima = fecha_desde
        fecha_ultimo_pago_vacacion = fecha_desde   
        fecha_ultimo_pago_cesantia_crudo = fecha_desde
        fecha_ultimo_pago_prima_crudo = fecha_desde
        fecha_ultimo_pago_vacacion_crudo = fecha_desde              
        # si ya se liquidaron primas o cesantias debemos sumar un dia, garantizar desde la programacion
        # que la fecha del ultimo pago sea fecha_hasta_periodo para tener el cuenta el 31 y al sumar
        # un dia nos de el mes siguiente
        if liquidacion.contrato.fecha_ultimo_pago_cesantia:
            fecha_ultimo_pago_cesantia = liquidacion.contrato.fecha_ultimo_pago_cesantia + timedelta(days=1)
            fecha_ultimo_pago_cesantia_crudo = liquidacion.contrato.fecha_ultimo_pago_cesantia
        if liquidacion.contrato.fecha_ultimo_pago_prima:
            fecha_ultimo_pago_prima = liquidacion.contrato.fecha_ultimo_pago_prima + timedelta(days=1)
            fecha_ultimo_pago_prima_crudo = liquidacion.contrato.fecha_ultimo_pago_prima
        if liquidacion.contrato.fecha_ultimo_pago_vacacion:
            fecha_ultimo_pago_vacacion = liquidacion.contrato.fecha_ultimo_pago_vacacion + timedelta(days=1)
            fecha_ultimo_pago_vacacion_crudo = liquidacion.contrato.fecha_ultimo_pago_vacacion

        dias = Utilidades.dias_prestacionales(fecha_ultimo_pago_cesantia.strftime("%Y-%m-%d"), fecha_hasta.strftime("%Y-%m-%d")) 
        dias_cesantia = Utilidades.dias_prestacionales(fecha_ultimo_pago_cesantia.strftime("%Y-%m-%d"), fecha_hasta.strftime("%Y-%m-%d")) 
        dias_prima = Utilidades.dias_prestacionales(fecha_ultimo_pago_prima.strftime("%Y-%m-%d"), fecha_hasta.strftime("%Y-%m-%d")) 
        dias_vacacion = Utilidades.dias_prestacionales(fecha_ultimo_pago_vacacion.strftime("%Y-%m-%d"), fecha_hasta.strftime("%Y-%m-%d")) 
        salario_promedio_cesantia = liquidacion.contrato.salario
        salario_promedio_prima = liquidacion.contrato.salario
        salario_promedio_vacacion = liquidacion.contrato.salario
        if liquidacion.contrato.auxilio_transporte:
            salario_promedio_cesantia = liquidacion.contrato.salario + auxilio_trasnporte
            salario_promedio_prima = liquidacion.contrato.salario + auxilio_trasnporte
        cesantia = round(salario_promedio_cesantia * dias_cesantia / 360)
        porcentaje_interes = ((dias_cesantia * 12) / 360) / 100
        interes = round(cesantia * porcentaje_interes)
        prima = round(salario_promedio_prima * dias_prima / 360)              
        vacacion = round((salario_promedio_vacacion * dias_vacacion) / 720)         
        total = cesantia + interes + prima + vacacion + total_adiciones - total_deducciones
        liquidacion.dias = dias
        liquidacion.dias_cesantia = dias_cesantia
        liquidacion.dias_prima = dias_prima
        liquidacion.dias_vacacion = dias_vacacion
        liquidacion.cesantia = cesantia
        liquidacion.interes = interes
        liquidacion.prima = prima
        liquidacion.vacacion = vacacion
        liquidacion.deduccion = total_deducciones
        liquidacion.adicion = total_adiciones
        liquidacion.total = total
        liquidacion.salario = liquidacion.contrato.salario
        liquidacion.fecha_ultimo_pago = liquidacion.contrato.fecha_ultimo_pago
        liquidacion.fecha_ultimo_pago_prima = fecha_ultimo_pago_prima_crudo
        liquidacion.fecha_ultimo_pago_cesantia = fecha_ultimo_pago_cesantia_crudo
        liquidacion.fecha_ultimo_pago_vacacion = fecha_ultimo_pago_vacacion_crudo
        liquidacion.save()             