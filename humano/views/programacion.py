from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.programacion import HumProgramacion
from humano.models.programacion_detalle import HumProgramacionDetalle
from humano.models.contrato import HumContrato
from humano.models.concepto import HumConcepto
from humano.models.concepto_nomina import HumConceptoNomina
from humano.models.adicional import HumAdicional
from humano.models.credito import HumCredito
from humano.models.novedad import HumNovedad
from general.models.documento_tipo import GenDocumentoTipo
from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from general.models.configuracion import GenConfiguracion
from general.models.contacto import GenContacto
from humano.serializers.programacion import HumProgramacionSerializador
from humano.serializers.programacion_detalle import HumProgramacionDetalleSerializador
from humano.serializers.programacion_detalle import  HumProgramacionDetalleImportarHorasSerializador
from general.serializers.documento import GenDocumentoSerializador
from general.serializers.documento_detalle import GenDocumentoDetalleSerializador
from general.formatos.programacion import FormatoProgramacion
from general.formatos.nomina import FormatoNomina
from django.db.models import Q, DecimalField, Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from decimal import Decimal, ROUND_HALF_UP
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db import transaction
import calendar
from django.template.loader import render_to_string
from utilidades.zinc import Zinc
from utilidades.utilidades import Utilidades
import base64
from io import BytesIO
import openpyxl

def horas_programacion(programacion_detalle):
    respuesta_horas = [
        {'cantidad':programacion_detalle.diurna, 'clave':0},
        {'cantidad':programacion_detalle.nocturna, 'clave':1},
        {'cantidad':programacion_detalle.festiva_diurna, 'clave':2},
        {'cantidad':programacion_detalle.festiva_nocturna, 'clave':3},
        {'cantidad':programacion_detalle.extra_diurna, 'clave':4},
        {'cantidad':programacion_detalle.extra_nocturna, 'clave':5},
        {'cantidad':programacion_detalle.extra_festiva_diurna, 'clave':6},
        {'cantidad':programacion_detalle.extra_festiva_nocturna, 'clave':7},
        {'cantidad':programacion_detalle.recargo_nocturno, 'clave':8},
        {'cantidad':programacion_detalle.recargo_festivo_diurno, 'clave':9},
        {'cantidad':programacion_detalle.recargo_festivo_nocturno, 'clave':10},
    ]
    return respuesta_horas

def datos_detalle(data_general, data, concepto):    
    data['operacion'] = concepto.operacion
    data['pago_operado'] = data['pago'] * concepto.operacion
    if concepto.operacion == 1:
        data['devengado'] = data['pago']
        data_general['devengado'] += data['pago']
    if concepto.operacion == -1:
        data['deduccion'] = data['pago']   
        data_general['deduccion'] += data['pago']     
    if concepto.ingreso_base_cotizacion:
        if concepto.id == 28:
            base =  round(data['cantidad'] * data['hora'])
            data['base_cotizacion'] = base
            data_general['base_cotizacion'] += base
            data_general['base_licencia'] += base
        else:
            data['base_cotizacion'] = data['pago']
            data_general['base_cotizacion'] += data['pago']
    if concepto.ingreso_base_prestacion:
        data['base_prestacion'] = data['pago']
        data_general['base_prestacion'] += data['pago']
    if concepto.ingreso_base_prestacion_vacacion:        
        data['base_prestacion_vacacion'] = data['pago']
        data_general['base_prestacion_vacacion'] += data['pago']        
    return data

def calcular_porcentaje_fondo(salario_minimo, base_cotizacion):
    salarios_minimos = base_cotizacion / salario_minimo
    porcentaje = 0
    if salarios_minimos >= 4 and salarios_minimos < 16:
        porcentaje = 1        
    if salarios_minimos >= 16 and salarios_minimos < 17:
        porcentaje = 1.2
    if salarios_minimos >= 17 and salarios_minimos < 18:
        porcentaje = 1.4
    if salarios_minimos >= 18 and salarios_minimos < 19:
        porcentaje = 1.6
    if salarios_minimos >= 19 and salarios_minimos < 20:
        porcentaje = 1.8
    if salarios_minimos >= 20:
        porcentaje = 2            
    return Decimal(porcentaje)

class HumProgramacionViewSet(viewsets.ModelViewSet):
    queryset = HumProgramacion.objects.all()
    serializer_class = HumProgramacionSerializador
    permission_classes = [permissions.IsAuthenticated]
    serializer_class_2 = HumProgramacionDetalleSerializador

    def perform_create(self, serializer):
        fecha_desde = serializer.validated_data.get('fecha_desde')
        fecha_hasta = serializer.validated_data.get('fecha_hasta')
        fecha_hasta_periodo = serializer.validated_data.get('fecha_hasta')                    
        if fecha_hasta.day == 30: 
            ultimo_dia = calendar.monthrange(fecha_hasta.year, fecha_hasta.month)[1]       
            if ultimo_dia == 31:
                fecha_hasta_periodo = fecha_hasta + timedelta(days=1)        
        diferencia = fecha_hasta - fecha_desde        
        dias_reales = diferencia.days + 1         
        dias = Utilidades.dias_prestacionales(fecha_desde.strftime("%Y-%m-%d"), fecha_hasta.strftime("%Y-%m-%d"))         
        serializer.save(dias=dias, dias_reales=dias_reales, fecha_hasta_periodo=fecha_hasta_periodo)

    def perform_update(self, serializer):
        fecha_desde = serializer.validated_data.get('fecha_desde')
        fecha_hasta = serializer.validated_data.get('fecha_hasta')
        fecha_hasta_periodo = serializer.validated_data.get('fecha_hasta')                    
        if fecha_hasta.day == 30: 
            ultimo_dia = calendar.monthrange(fecha_hasta.year, fecha_hasta.month)[1]       
            if ultimo_dia == 31:
                fecha_hasta_periodo = fecha_hasta + timedelta(days=1)        
        #diferencia = fecha_hasta - fecha_desde        
        #dias = diferencia.days + 1         
        dias = Utilidades.dias_prestacionales(fecha_desde.strftime("%Y-%m-%d"), fecha_hasta.strftime("%Y-%m-%d"))         
        serializer.save(dias=dias, fecha_hasta_periodo=fecha_hasta_periodo)

    def destroy(self, request, *args, **kwargs):        
        instance = self.get_object()
        if instance.estado_aprobado:
                return Response({'mensaje': 'No se puede eliminar un documento aprobado.'}, status=status.HTTP_400_BAD_REQUEST)
        programacionDetalles = HumProgramacionDetalle.objects.filter(programacion_id=instance.id).first()
        if programacionDetalles:
            return Response({'mensaje': 'La programacion tiene detalles y no se puede eliminar'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"], url_path=r'cargar-contrato',)
    def cargar_contrato(self, request):
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                programacion = HumProgramacion.objects.get(pk=id)                                
                if programacion.estado_generado == False:
                    with transaction.atomic():
                        cantidad = programacion.contratos
                        configuracion = GenConfiguracion.objects.filter(pk=1).values('hum_factor', 'hum_auxilio_transporte')[0]                
                        # nomina
                        if programacion.pago_tipo_id == 1:
                            contratos = HumContrato.objects.filter(
                                    grupo_id=programacion.grupo_id                        
                                    ).filter(
                                        Q(fecha_ultimo_pago__isnull=True) | Q(fecha_ultimo_pago__lt=programacion.fecha_hasta) | Q(fecha_desde=programacion.fecha_hasta_periodo) | Q(fecha_desde=programacion.fecha_hasta)
                                    ).filter(
                                        fecha_desde__lte=programacion.fecha_hasta_periodo
                                    ).filter(
                                        Q(fecha_hasta__gte=programacion.fecha_desde) | Q(estado_terminado=False))
                            #print(contratos.query)                                             
                            for contrato in contratos:
                                contrato_validar = HumProgramacionDetalle.objects.filter(programacion_id=programacion.id, contrato_id=contrato.id).exists()
                                if not contrato_validar:
                                    ingreso = False
                                    if contrato.fecha_desde >= programacion.fecha_desde and contrato.fecha_desde <= programacion.fecha_hasta_periodo:
                                        ingreso = True                
                                    retiro = False
                                    if contrato.fecha_hasta <= programacion.fecha_hasta and contrato.fecha_hasta >= programacion.fecha_desde and contrato.contrato_tipo_id != 1:
                                        retiro = True
                                    data = {
                                        'programacion': programacion.id,
                                        'contrato': contrato.id,
                                        'salario': contrato.salario,
                                        'pago_horas': programacion.pago_horas,
                                        'pago_auxilio_transporte': programacion.pago_auxilio_transporte,
                                        'pago_incapacidad': programacion.pago_incapacidad,
                                        'pago_licencia': programacion.pago_licencia,
                                        'pago_vacacion': programacion.pago_vacacion,
                                        'descuento_salud': programacion.descuento_salud,
                                        'descuento_pension': programacion.descuento_pension,
                                        'descuento_fondo_solidaridad': programacion.descuento_fondo_solidaridad,
                                        'descuento_retencion_fuente': programacion.descuento_retencion_fuente,                        
                                        'descuento_credito': programacion.descuento_credito,
                                        'descuento_embargo': programacion.descuento_embargo,
                                        'adicional': programacion.adicional,
                                        'ingreso': ingreso,
                                        'retiro': retiro,
                                        'error_terminacion': False,
                                        'base_cotizacion_acumulado': 0,
                                        'deduccion_fondo_pension_acumulado': 0
                                    }
                                    if contrato.contrato_tipo_id == 5 or contrato.contrato_tipo_id == 6:
                                        data['descuento_pension'] = False
                                        data['descuento_salud'] = False
                                        data['pago_auxilio_transporte'] = False
                            
                                    if contrato.pension_id == 4:
                                        data['descuento_pension'] = False
                                    
                                    fecha_desde = contrato.fecha_desde
                                    if fecha_desde < programacion.fecha_desde:
                                        fecha_desde = programacion.fecha_desde
                                    data['fecha_desde'] = fecha_desde

                                    error_terminacion = False    
                                    fecha_hasta = contrato.fecha_hasta
                                    if contrato.contrato_tipo_id == 1:
                                        fecha_hasta = programacion.fecha_hasta
                                    else:
                                        if contrato.estado_terminado == False:
                                            if contrato.fecha_hasta < programacion.fecha_desde:
                                                fecha_hasta = programacion.fecha_desde
                                                error_terminacion = True
                                    if fecha_hasta > programacion.fecha_hasta:
                                        fecha_hasta = programacion.fecha_hasta
                                                
                                    data['fecha_hasta'] = fecha_hasta  
                                    data['error_terminacion'] = error_terminacion                         
                                    dias_novedad = 0
                                    novedades = HumNovedad.objects.filter(
                                        contrato_id = contrato.id,
                                        fecha_desde__lte=programacion.fecha_hasta, 
                                        fecha_hasta__gte=programacion.fecha_desde                                
                                        )
                                    for novedad in novedades:
                                        fecha_desde_novedad = fecha_desde
                                        fecha_hasta_novedad = fecha_hasta
                                        if novedad.fecha_desde > fecha_desde:
                                            fecha_desde_novedad = novedad.fecha_desde                                

                                        if novedad.fecha_hasta < fecha_hasta:
                                            fecha_hasta_novedad = novedad.fecha_hasta  

                                        diferencia = fecha_hasta_novedad - fecha_desde_novedad
                                        dias_novedad += diferencia.days + 1


                                    diferencia = fecha_hasta - fecha_desde
                                    dias = diferencia.days + 1
                                    dias = dias - dias_novedad                                    
                                    dias_febrero = 0
                                    if programacion.fecha_desde.month == 2 and programacion.fecha_hasta.month == 2:
                                        if dias + dias_novedad == programacion.dias_reales:
                                            if programacion.fecha_hasta.day == 28:
                                                dias_febrero += 2
                                            elif programacion.fecha_hasta.day == 29:
                                                dias_febrero += 1
                                    dias += dias_febrero
                                    if dias < 0:
                                        dias = 0
                                    if error_terminacion:
                                        dias = 0
                                    data['dias'] = dias
                                    data['dias_transporte'] = dias
                                    data['dias_novedad'] = dias_novedad
                                    data['diurna'] = dias * configuracion['hum_factor']
                                    if contrato.tiempo_id == 2:
                                        data['diurna'] = round(dias * (configuracion['hum_factor'] / 2), 3)
                                    
                                    fecha_desde_mes = programacion.fecha_desde.replace(day=1)
                                    fecha_hasta_mes = (programacion.fecha_desde.replace(day=1) + relativedelta(months=1)) - relativedelta(days=1)                              
                                    documento_detalle = GenDocumentoDetalle.objects.filter(
                                        documento__fecha__gte=fecha_desde_mes,
                                        documento__fecha__lte=fecha_hasta_mes,                                                                
                                        documento__contrato_id=contrato.id,
                                        documento__estado_aprobado=True
                                    ).aggregate(
                                        ibc=Coalesce(Sum('base_cotizacion'), 0, output_field=DecimalField())
                                    )
                                    data['base_cotizacion_acumulado'] = documento_detalle['ibc']
                                    documento_detalle = GenDocumentoDetalle.objects.filter(
                                        documento__fecha__gte=fecha_desde_mes,
                                        documento__fecha__lte=fecha_hasta_mes,                                                                
                                        documento__contrato_id=contrato.id,
                                        documento__estado_aprobado=True,
                                        concepto_id=20
                                    ).aggregate(
                                        pago=Coalesce(Sum('pago'), 0, output_field=DecimalField())
                                    )                                
                                    data['deduccion_fondo_pension_acumulado'] = documento_detalle['pago']
                                    programacion_detalle_serializador = HumProgramacionDetalleSerializador(data=data)
                                    if programacion_detalle_serializador.is_valid():
                                        programacion_detalle_serializador.save()
                                        cantidad += 1
                                    else:
                                        return Response({'validaciones':programacion_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)
                        
                        # primas
                        if programacion.pago_tipo_id == 2:
                            contratos = HumContrato.objects.filter(
                                    grupo_id=programacion.grupo_id                        
                                    ).filter(
                                        fecha_desde__lte=programacion.fecha_hasta_periodo
                                    ).filter(
                                        estado_terminado=False) 
                            #print(contratos.query)
                            for contrato in contratos:
                                contrato_validar = HumProgramacionDetalle.objects.filter(programacion_id=programacion.id, contrato_id=contrato.id).exists()
                                if not contrato_validar:
                                    ingreso = False
                                    if contrato.fecha_desde >= programacion.fecha_desde and contrato.fecha_desde <= programacion.fecha_hasta_periodo:
                                        ingreso = True                

                                    data = {
                                        'programacion': programacion.id,
                                        'contrato': contrato.id,
                                        'salario': contrato.salario,
                                        'dias_transporte': 0,
                                        'pago_horas': programacion.pago_horas,
                                        'pago_auxilio_transporte': programacion.pago_auxilio_transporte,
                                        'pago_incapacidad': programacion.pago_incapacidad,
                                        'pago_licencia': programacion.pago_licencia,
                                        'pago_vacacion': programacion.pago_vacacion,
                                        'descuento_salud': programacion.descuento_salud,
                                        'descuento_pension': programacion.descuento_pension,
                                        'descuento_fondo_solidaridad': programacion.descuento_fondo_solidaridad,
                                        'descuento_retencion_fuente': programacion.descuento_retencion_fuente,                        
                                        'descuento_credito': programacion.descuento_credito,
                                        'descuento_embargo': programacion.descuento_embargo,
                                        'adicional': programacion.adicional,
                                        'ingreso': ingreso,
                                        'retiro': False
                                    }                    
                                    
                                    fecha_desde = contrato.fecha_desde
                                    if fecha_desde < programacion.fecha_desde:
                                        fecha_desde = programacion.fecha_desde
                                    data['fecha_desde'] = fecha_desde
                                        
                                    fecha_hasta = contrato.fecha_hasta
                                    if contrato.contrato_tipo_id == 1:
                                        fecha_hasta = programacion.fecha_hasta
                                    if fecha_hasta > programacion.fecha_hasta:
                                        fecha_hasta = programacion.fecha_hasta
                                    data['fecha_hasta'] = fecha_hasta                                

                                    dias = Utilidades.dias_prestacionales(data['fecha_desde'].strftime('%Y-%m-%d'),
                                                                                    data['fecha_hasta'].strftime('%Y-%m-%d'))                                
                                    salario_promedio_primas = 0
                                    if contrato.auxilio_transporte:
                                        salario_promedio_primas = contrato.salario + configuracion['hum_auxilio_transporte']
                                    else:
                                        salario_promedio_primas = contrato.salario


                                    data['dias'] = dias
                                    data['salario_promedio'] = salario_promedio_primas            
                                    programacion_detalle_serializador = HumProgramacionDetalleSerializador(data=data)
                                    if programacion_detalle_serializador.is_valid():
                                        programacion_detalle_serializador.save()
                                        cantidad += 1
                                    else:
                                        return Response({'validaciones':programacion_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                    

                        # cesantias
                        if programacion.pago_tipo_id == 3:
                            contratos = HumContrato.objects.filter(
                                    grupo_id=programacion.grupo_id                        
                                    ).filter(
                                        fecha_desde__lte=programacion.fecha_hasta_periodo
                                    ).filter(
                                        estado_terminado=False) 
                            #print(contratos.query)
                            for contrato in contratos:
                                contrato_validar = HumProgramacionDetalle.objects.filter(programacion_id=programacion.id, contrato_id=contrato.id).exists()
                                if not contrato_validar:
                                    ingreso = False
                                    if contrato.fecha_desde >= programacion.fecha_desde and contrato.fecha_desde <= programacion.fecha_hasta_periodo:
                                        ingreso = True                

                                    data = {
                                        'programacion': programacion.id,
                                        'contrato': contrato.id,
                                        'salario': contrato.salario,
                                        'dias_transporte': 0,
                                        'pago_horas': programacion.pago_horas,
                                        'pago_auxilio_transporte': programacion.pago_auxilio_transporte,
                                        'pago_incapacidad': programacion.pago_incapacidad,
                                        'pago_licencia': programacion.pago_licencia,
                                        'pago_vacacion': programacion.pago_vacacion,
                                        'descuento_salud': programacion.descuento_salud,
                                        'descuento_pension': programacion.descuento_pension,
                                        'descuento_fondo_solidaridad': programacion.descuento_fondo_solidaridad,
                                        'descuento_retencion_fuente': programacion.descuento_retencion_fuente,                        
                                        'descuento_credito': programacion.descuento_credito,
                                        'descuento_embargo': programacion.descuento_embargo,
                                        'adicional': programacion.adicional,
                                        'ingreso': ingreso,
                                        'retiro': False
                                    }                    
                                    
                                    fecha_desde = contrato.fecha_desde
                                    if fecha_desde < programacion.fecha_desde:
                                        fecha_desde = programacion.fecha_desde
                                    data['fecha_desde'] = fecha_desde
                                        
                                    fecha_hasta = contrato.fecha_hasta
                                    if contrato.contrato_tipo_id == 1:
                                        fecha_hasta = programacion.fecha_hasta
                                    if fecha_hasta > programacion.fecha_hasta:
                                        fecha_hasta = programacion.fecha_hasta
                                    data['fecha_hasta'] = fecha_hasta                                

                                    dias = Utilidades.dias_prestacionales(data['fecha_desde'].strftime('%Y-%m-%d'),
                                                                                    data['fecha_hasta'].strftime('%Y-%m-%d'))                                
                                    if contrato.auxilio_transporte:
                                        salario_promedio_cesantias = contrato.salario + configuracion['hum_auxilio_transporte']
                                    else:
                                        salario_promedio_cesantias = contrato.salario


                                    data['dias'] = dias
                                    data['salario_promedio'] = salario_promedio_cesantias            
                                    programacion_detalle_serializador = HumProgramacionDetalleSerializador(data=data)
                                    if programacion_detalle_serializador.is_valid():
                                        programacion_detalle_serializador.save()
                                        cantidad += 1
                                    else:
                                        return Response({'validaciones':programacion_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST) 

                        programacion.contratos = cantidad
                        programacion.save()
                        return Response({'contratos': cantidad}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'La programacion ya esta generada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumProgramacion.DoesNotExist:
            return Response({'mensaje':'La programacion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)    
        
    @action(detail=False, methods=["post"], url_path=r'generar',)
    def generar(self, request):
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                programacion = HumProgramacion.objects.get(pk=id)
                if programacion.estado_generado == False and programacion.estado_aprobado == False:
                    with transaction.atomic():
                        total_programacion = 0
                        devengado_programacion = 0
                        deduccion_programacion = 0
                        conceptos_nomina = HumConceptoNomina.objects.all().order_by('id')
                        configuracion = GenConfiguracion.objects.filter(pk=1).values('hum_factor', 'hum_auxilio_transporte', 'hum_salario_minimo')[0]
                        programacion_detalles = HumProgramacionDetalle.objects.filter(programacion_id=id)                                           
                        for programacion_detalle in programacion_detalles:                                  
                            documento_tipo = 14
                            if programacion.pago_tipo_id == 2:
                                documento_tipo = 20
                            if programacion.pago_tipo_id == 3:
                                documento_tipo = 21
                            data = {
                                'programacion_detalle': programacion_detalle.id,
                                'documento_tipo': documento_tipo,
                                'empresa': 1,
                                'fecha': programacion_detalle.fecha_desde,
                                'fecha_vence': programacion_detalle.fecha_desde,
                                'fecha_contable': programacion_detalle.fecha_desde,
                                'fecha_hasta': programacion_detalle.fecha_hasta,
                                'contrato': programacion_detalle.contrato_id,
                                'contacto': programacion_detalle.contrato.contacto_id,
                                'grupo': programacion_detalle.contrato.grupo_id,
                                'periodo': programacion.periodo_id,
                                'salario': programacion_detalle.salario,
                                'dias': programacion_detalle.dias                    
                            }
                            documento_serializador = GenDocumentoSerializador(data=data)
                            if documento_serializador.is_valid():
                                documento = documento_serializador.save()
                                # Variables generales
                                base_salario_minimo = (configuracion['hum_salario_minimo']/30) * programacion_detalle.dias
                                contrato = programacion_detalle.contrato
                                valor_dia_contrato = programacion_detalle.salario / 30
                                # No quitar este codigo comentado Mario
                                #if contrato.tiempo_id == 2:
                                #    valor_dia_contrato = (programacion_detalle.salario * 2) / 30
                                valor_hora_contrato = valor_dia_contrato / configuracion['hum_factor']
                                data_general = {
                                    'devengado': 0,
                                    'deduccion': 0,
                                    'base_cotizacion': 0,
                                    'base_prestacion': 0,
                                    'base_prestacion_vacacion': 0,
                                    'base_licencia': 0
                                }
                                data_general_detalle = {
                                    'tipo_registro': 'N',
                                    'documento': documento.id,
                                    'contacto': programacion_detalle.contrato.contacto_id                                    
                                }

                                # Nomina
                                if programacion.pago_tipo_id == 1:
                                    horas = horas_programacion(programacion_detalle)
                                    # Horas y salarios
                                    if programacion_detalle.pago_horas:                                
                                        for hora in horas:
                                            if hora['cantidad'] > 0:
                                                concepto_nomina = conceptos_nomina[hora['clave']] 
                                                concepto = concepto_nomina.concepto                                                                    
                                                valor_hora_detalle = (valor_hora_contrato * concepto.porcentaje) / 100                                                                                                                                                
                                                valor_hora_detalle = Decimal(valor_hora_detalle).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
                                                pago = round(valor_hora_detalle * hora['cantidad'])
                                                data = data_general_detalle.copy() 
                                                data['cantidad'] = hora['cantidad']
                                                data['hora'] = valor_hora_detalle
                                                data['dias'] = programacion_detalle.dias
                                                data['porcentaje'] = concepto.porcentaje
                                                data['pago'] = pago
                                                data['concepto'] = concepto_nomina.concepto_id                                                 
                                                if hora['clave'] == 0:
                                                    data['dias'] = programacion_detalle.dias

                                                datos_detalle(data_general, data, concepto)
                                                documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                                if documento_detalle_serializador.is_valid():
                                                    documento_detalle_serializador.save()
                                                else:
                                                    return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)  

                                    # Novedades
                                    if programacion_detalle.pago_incapacidad or programacion_detalle.pago_licencia or programacion_detalle.pago_vacacion:                                                            
                                        novedades = HumNovedad.objects.filter(
                                            contrato_id = contrato.id,
                                            fecha_desde__lte=programacion.fecha_hasta, 
                                            fecha_hasta__gte=programacion.fecha_desde                                
                                            )
                                        for novedad in novedades:
                                            dia31 = 0
                                            fecha_desde_novedad = programacion.fecha_desde
                                            fecha_hasta_novedad = programacion.fecha_hasta
                                            # Si la novedad es mayor o igual a la fecha y es una quincena con 31
                                            if programacion.fecha_hasta_periodo.day == 31:
                                                if novedad.fecha_hasta >= programacion.fecha_hasta_periodo:
                                                    dia31 = 1
                                            if novedad.fecha_desde > programacion.fecha_desde:
                                                fecha_desde_novedad = novedad.fecha_desde                                

                                            if novedad.fecha_hasta < programacion.fecha_hasta:
                                                fecha_hasta_novedad = novedad.fecha_hasta  

                                            diferencia = fecha_hasta_novedad - fecha_desde_novedad
                                            dias_novedad = diferencia.days + 1 
                                            pago = 0
                                            # Incapacidad
                                            if novedad.novedad_tipo_id in [1, 2]:
                                                if novedad.dias_empresa > 0:
                                                    fecha_desde_empresa = programacion.fecha_desde
                                                    if novedad.fecha_desde_empresa > programacion.fecha_desde:
                                                        fecha_desde_empresa = novedad.fecha_desde_empresa                               
                                                    fecha_hasta_empresa = programacion.fecha_hasta
                                                    if novedad.fecha_hasta_empresa < programacion.fecha_hasta:
                                                        fecha_hasta_empresa = novedad.fecha_hasta_empresa
                                                    diferencia = fecha_hasta_empresa - fecha_desde_empresa
                                                    dias_empresa = diferencia.days + 1
                                                    if dias_empresa > 0:                                                
                                                        concepto = novedad.novedad_tipo.concepto
                                                        horas = dias_empresa * configuracion['hum_factor']                                                                                                                                                
                                                        pago = round(novedad.hora_empresa * horas)                                                                                 
                                                        data = data_general_detalle.copy()
                                                        data['dias'] = dias_empresa
                                                        data['hora'] = novedad.hora_empresa
                                                        data['cantidad'] = horas
                                                        data['pago'] = pago
                                                        data['porcentaje'] = concepto.porcentaje
                                                        data['concepto'] = novedad.novedad_tipo.concepto_id
                                                        data['novedad'] = novedad.id
                                                        data = datos_detalle(data_general, data, concepto)
                                                        documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                                        if documento_detalle_serializador.is_valid():
                                                            documento_detalle_serializador.save()
                                                        else:
                                                            return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)  
                                                
                                                if novedad.dias_entidad > 0:
                                                    fecha_desde_entidad = programacion.fecha_desde
                                                    if novedad.fecha_desde_entidad > programacion.fecha_desde:
                                                        fecha_desde_entidad = novedad.fecha_desde_entidad                               
                                                    fecha_hasta_entidad = programacion.fecha_hasta
                                                    if novedad.fecha_hasta_entidad < programacion.fecha_hasta:
                                                        fecha_hasta_entidad = novedad.fecha_hasta_entidad
                                                    diferencia = fecha_hasta_entidad - fecha_desde_entidad
                                                    dias_entidad = diferencia.days + 1
                                                    if dias_entidad > 0:                                                
                                                        concepto = novedad.novedad_tipo.concepto2
                                                        horas = dias_entidad * configuracion['hum_factor']                                                                                                                                                
                                                        pago = round(novedad.hora_entidad * horas)                                                                                 
                                                        data = data_general_detalle.copy()
                                                        data['dias'] = dias_entidad
                                                        data['hora'] = novedad.hora_entidad
                                                        data['cantidad'] = horas
                                                        data['pago'] = pago
                                                        data['porcentaje'] = concepto.porcentaje
                                                        data['concepto'] = novedad.novedad_tipo.concepto2_id
                                                        data['novedad'] = novedad.id
                                                        data = datos_detalle(data_general, data, concepto)
                                                        documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                                        if documento_detalle_serializador.is_valid():
                                                            documento_detalle_serializador.save()
                                                        else:
                                                            return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                                
                                            # Licencia
                                            if novedad.novedad_tipo_id in [3, 4, 5, 6]:
                                                if dias_novedad > 0:               
                                                    hora = 0
                                                    if novedad.novedad_tipo_id in [3]:
                                                        hora = novedad.hora_entidad
                                                    if novedad.novedad_tipo_id in [4, 5]:
                                                        hora = novedad.hora_empresa
                                                    if novedad.novedad_tipo_id in [6]:
                                                        hora = round(valor_hora_contrato, 6)
                                                    concepto = novedad.novedad_tipo.concepto
                                                    horas = dias_novedad * configuracion['hum_factor']                                                                                                                                                
                                                    pago = round(hora * horas)
                                                    if novedad.novedad_tipo_id == 6:
                                                        pago = 0
                                                    data = data_general_detalle.copy()
                                                    data['dias'] = dias_novedad
                                                    data['hora'] = hora
                                                    data['cantidad'] = horas
                                                    data['pago'] = pago
                                                    data['porcentaje'] = concepto.porcentaje
                                                    data['concepto'] = novedad.novedad_tipo.concepto_id
                                                    data['novedad'] = novedad.id
                                                    data = datos_detalle(data_general, data, concepto)
                                                    documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                                    if documento_detalle_serializador.is_valid():
                                                        documento_detalle_serializador.save()
                                                    else:
                                                        return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)
                                            # Vacacion
                                            if novedad.novedad_tipo_id == 7:
                                                # Vacaciones disfrutadas
                                                dias_novedad_pago = dias_novedad + dia31
                                                concepto = novedad.novedad_tipo.concepto
                                                pago = round(dias_novedad_pago * novedad.pago_dia_disfrute)                                    
                                                data = data_general_detalle.copy()
                                                data['dias'] = dias_novedad
                                                data['pago'] = pago
                                                data['concepto'] = novedad.novedad_tipo.concepto_id
                                                data['novedad'] = novedad.id
                                                data = datos_detalle(data_general, data, concepto)
                                                documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                                if documento_detalle_serializador.is_valid():
                                                    documento_detalle_serializador.save()
                                                else:
                                                    return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)  

                                                # Vacaciones en dinero
                                                concepto = novedad.novedad_tipo.concepto2
                                                pago = round(dias_novedad_pago * novedad.pago_dia_dinero)                                    
                                                data = data_general_detalle.copy()
                                                data['dias'] = dias_novedad
                                                data['pago'] = pago
                                                data['concepto'] = novedad.novedad_tipo.concepto2_id
                                                data['novedad'] = novedad.id
                                                data = datos_detalle(data_general, data, concepto)
                                                documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                                if documento_detalle_serializador.is_valid():
                                                    documento_detalle_serializador.save()
                                                else:
                                                    return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                                                           
                                                            
                                    # Auxilio transporte
                                    if programacion_detalle.pago_auxilio_transporte:
                                        if contrato.auxilio_transporte:
                                            dia_auxilio_transporte = configuracion['hum_auxilio_transporte'] / 30
                                            concepto_nomina = conceptos_nomina[11]
                                            concepto = concepto_nomina.concepto
                                            pago = round(dia_auxilio_transporte * programacion_detalle.dias_transporte)                                    
                                            if pago > 0:
                                                data = data_general_detalle.copy()
                                                data['pago'] = pago
                                                data['dias'] = programacion_detalle.dias_transporte
                                                data['concepto'] = concepto.id
                                                datos_detalle(data_general, data, concepto)
                                                documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                                if documento_detalle_serializador.is_valid():
                                                    documento_detalle_serializador.save()
                                                else:
                                                    return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)
                                                                
                                # Prima
                                if programacion.pago_tipo_id == 2:
                                    if programacion.pago_prima:
                                        prima = (programacion_detalle.salario_promedio * programacion_detalle.dias) / 360
                                        concepto_nomina = conceptos_nomina[12]
                                        concepto = concepto_nomina.concepto
                                        pago = round(prima)                                    
                                        if pago > 0:
                                            data = data_general_detalle.copy()
                                            data['pago'] = pago
                                            data['dias'] = programacion_detalle.dias
                                            data['concepto'] = concepto.id
                                            datos_detalle(data_general, data, concepto)
                                            documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                            if documento_detalle_serializador.is_valid():
                                                documento_detalle_serializador.save()
                                            else:
                                                return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                
                                
                                # Cesantias
                                if programacion.pago_tipo_id == 3:
                                    # Cesantia                                
                                    cesantia = (programacion_detalle.salario_promedio * programacion_detalle.dias) / 360                                
                                    if programacion.pago_cesantia:
                                        concepto_cesantias = conceptos_nomina[13].concepto                                
                                        pago = round(cesantia)                                    
                                        if pago > 0:
                                            data = data_general_detalle.copy()
                                            data['pago'] = pago
                                            data['dias'] = programacion_detalle.dias
                                            data['concepto'] = concepto_cesantias.id
                                            datos_detalle(data_general, data, concepto_cesantias)
                                            documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                            if documento_detalle_serializador.is_valid():
                                                documento_detalle_serializador.save()
                                            else:
                                                return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)
                                        
                                    # Interes
                                    if programacion.pago_interes:
                                        concepto_interes = conceptos_nomina[14].concepto                                      
                                        porcentaje_interes = ((programacion_detalle.dias * 12) / 360) / 100
                                        insteres = cesantia * porcentaje_interes
                                        pago = round(insteres)                                    
                                        if pago > 0:
                                            data = data_general_detalle.copy()
                                            data['pago'] = pago
                                            data['dias'] = programacion_detalle.dias
                                            data['concepto'] = concepto_interes.id
                                            datos_detalle(data_general, data, concepto_interes)
                                            documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                            if documento_detalle_serializador.is_valid():
                                                documento_detalle_serializador.save()
                                            else:
                                                return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                                                  

                                # Adicionales
                                if programacion_detalle.adicional:
                                    filtro_base = HumAdicional.objects.filter(
                                        inactivo=False,                                         
                                        contrato_id=programacion_detalle.contrato_id
                                    )
                                    if programacion.pago_tipo_id == 1:
                                        adicionales = filtro_base.filter(Q(permanente=True) | Q(programacion_id=programacion.id))
                                    else:
                                        adicionales = filtro_base.filter(Q(programacion_id=programacion.id))

                                    for adicional in adicionales:                        
                                        concepto = adicional.concepto
                                        if adicional.aplica_dia_laborado:                                                                
                                            valor_adicional_dia = adicional.valor / programacion.dias;                        
                                            valor_adicional = valor_adicional_dia * programacion_detalle.dias
                                        else:
                                            valor_adicional = adicional.valor
                                        data = data_general_detalle.copy()
                                        data['pago'] = round(valor_adicional)
                                        data['concepto'] = adicional.concepto_id
                                        data['detalle'] = adicional.detalle
                                        data = datos_detalle(data_general, data, concepto)
                                        documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                        if documento_detalle_serializador.is_valid():
                                            documento_detalle_serializador.save()
                                        else:
                                            return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST) 

                                #creditos
                                if programacion_detalle.descuento_credito:
                                    creditos = HumCredito.objects.filter(
                                            inactivo = False, 
                                            pagado = False,
                                            contrato_id = programacion_detalle.contrato_id
                                        )
                                    if programacion.pago_tipo_id == 2:
                                        creditos = creditos.filter(aplica_prima=True)
                                    if programacion.pago_tipo_id == 3:
                                        creditos = creditos.filter(aplica_cesantia=True)
                                    for credito in creditos: 
                                        if credito.saldo > 0:                       
                                            concepto = credito.concepto
                                            if credito.saldo >= credito.cuota:
                                                pago = credito.cuota
                                            else:
                                                pago = credito.saldo;                                                                                                
                                            data = data_general_detalle.copy()
                                            data['pago'] = round(pago)
                                            data['concepto'] = credito.concepto_id
                                            data['credito'] = credito.id
                                            data = datos_detalle(data_general, data, concepto)
                                            documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                            if documento_detalle_serializador.is_valid():
                                                documento_detalle_serializador.save()
                                            else:
                                                return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)

                                # Salud
                                if programacion_detalle.descuento_salud:
                                    salud = contrato.salud
                                    if salud:
                                        if salud.porcentaje_empleado > 0:                                                                                
                                            concepto = salud.concepto     
                                            base = data_general['base_cotizacion'] - data_general['base_licencia']
                                            if contrato.tiempo_id == 2:
                                                if base < base_salario_minimo:
                                                    base = base_salario_minimo
                                            if base > 0:                                  
                                                pago = round((base * salud.porcentaje_empleado) / 100)
                                                data = data_general_detalle.copy()
                                                data['porcentaje'] = salud.porcentaje_empleado
                                                data['pago'] = pago
                                                data['concepto'] = concepto.id
                                                contacto = GenContacto.objects.filter(numero_identificacion=programacion_detalle.contrato.entidad_salud.numero_identificacion).first()
                                                if contacto:
                                                    data['contacto'] = contacto.id
                                                else:
                                                    data['contacto'] = None
                                                datos_detalle(data_general, data, concepto)
                                                documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                                if documento_detalle_serializador.is_valid():
                                                    documento_detalle_serializador.save()
                                                else:
                                                    return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)

                                # Pension
                                if programacion_detalle.descuento_pension:
                                    pension = contrato.pension
                                    if pension:
                                        if pension.porcentaje_empleado > 0:  
                                            if data_general['base_cotizacion'] > 0:
                                                concepto = pension.concepto  
                                                base = data_general['base_cotizacion'] 
                                                if contrato.tiempo_id == 2:
                                                    if base < base_salario_minimo:
                                                        base = base_salario_minimo 
                                                if base > 0:
                                                    pago = round((base * pension.porcentaje_empleado) / 100)                                        
                                                    data = data_general_detalle.copy()
                                                    data['porcentaje'] = pension.porcentaje_empleado
                                                    data['pago'] = pago
                                                    data['concepto'] = concepto.id
                                                    contacto = GenContacto.objects.filter(numero_identificacion=programacion_detalle.contrato.entidad_pension.numero_identificacion).first()
                                                    if contacto:
                                                        data['contacto'] = contacto.id
                                                    else:
                                                        data['contacto'] = None                                                    
                                                    datos_detalle(data_general, data, concepto)
                                                    documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                                    if documento_detalle_serializador.is_valid():
                                                        documento_detalle_serializador.save()
                                                    else:
                                                        return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)

                                # Fondo solidaridad
                                if programacion_detalle.descuento_fondo_solidaridad:
                                    pension = contrato.pension
                                    if pension:
                                        tope_fondo = configuracion['hum_salario_minimo'] * 4
                                        base_cotizacion_total = data_general['base_cotizacion'] + programacion_detalle.base_cotizacion_acumulado
                                        if base_cotizacion_total >= tope_fondo:    
                                            porcentaje_fondo = calcular_porcentaje_fondo(configuracion['hum_salario_minimo'], base_cotizacion_total)                                      
                                            if porcentaje_fondo > 0:
                                                if base_cotizacion_total > configuracion['hum_salario_minimo'] * 25:
                                                    round(base_cotizacion_total = configuracion['hum_salario_minimo'] * 25)                                            
                                                concepto = HumConcepto.objects.get(pk=20)                                              
                                                pago = round((base_cotizacion_total * porcentaje_fondo) / 100) 
                                                pago = round(pago - programacion_detalle.deduccion_fondo_pension_acumulado)
                                                if pago > 0:
                                                    data = data_general_detalle.copy()
                                                    data['porcentaje'] = porcentaje_fondo
                                                    data['pago'] = pago
                                                    data['concepto'] = concepto.id
                                                    contacto = GenContacto.objects.filter(numero_identificacion=programacion_detalle.contrato.entidad_pension.numero_identificacion).first()
                                                    if contacto:
                                                        data['contacto'] = contacto.id
                                                    else:
                                                        data['contacto'] = None                                                     
                                                    datos_detalle(data_general, data, concepto)
                                                    documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                                    if documento_detalle_serializador.is_valid():
                                                        documento_detalle_serializador.save()
                                                    else:
                                                        return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)

                                total = data_general['devengado'] - data_general['deduccion']
                                devengado = data_general['devengado']
                                deduccion = data_general['deduccion']                                
                                provision_cesantia = data_general['base_prestacion'] * 0.0833
                                provision_interes = provision_cesantia * 0.12
                                provision_prima = data_general['base_prestacion'] * 0.0833
                                provision_vacacion = data_general['base_prestacion_vacacion'] * 0.0417
                                documento.provision_cesantia = round(provision_cesantia)
                                documento.provision_interes = round(provision_interes)
                                documento.provision_prima = round(provision_prima)
                                documento.provision_vacacion = round(provision_vacacion)
                                documento.base_cotizacion = data_general['base_cotizacion']
                                documento.base_prestacion = data_general['base_prestacion']
                                documento.base_prestacion_vacacion = data_general['base_prestacion_vacacion']
                                documento.devengado = devengado
                                documento.deduccion = deduccion
                                documento.total = total
                                documento.save()

                                programacion_detalle.devengado = devengado
                                programacion_detalle.deduccion = deduccion
                                programacion_detalle.total = total
                                programacion_detalle.save()
                                total_programacion += total
                                devengado_programacion += devengado
                                deduccion_programacion += deduccion

                            else:
                                return Response({'validaciones':documento_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)  

                        programacion.estado_generado = True  
                        programacion.total = total_programacion
                        programacion.devengado = devengado_programacion
                        programacion.deduccion = deduccion_programacion
                        programacion.save()
                        return Response({'total': total_programacion, 'devengado': devengado_programacion, 'deduccion': deduccion_programacion}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'La programacion ya esta generada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumProgramacion.DoesNotExist:
            return Response({'mensaje':'La programacion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)      

    @action(detail=False, methods=["post"], url_path=r'desgenerar',)
    def desgenerar(self, request):             
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                programacion = HumProgramacion.objects.get(pk=id)
                if programacion.estado_aprobado == False and programacion.estado_generado == True:
                    programacion_detalles = HumProgramacionDetalle.objects.filter(programacion_id=id)
                    for programacion_detalle in programacion_detalles:
                        documentos = GenDocumento.objects.filter(programacion_detalle_id=programacion_detalle.id)
                        for documento in documentos:
                            documento_detalles = GenDocumentoDetalle.objects.filter(documento_id=documento.id)
                            documento_detalles.delete()
                        documentos.delete()
                        programacion_detalle.devengado = 0
                        programacion_detalle.deduccion = 0
                        programacion_detalle.total = 0
                        programacion_detalle.save()
                    programacion.estado_generado = False
                    programacion.total = 0
                    programacion.devengado = 0
                    programacion.deduccion = 0
                    programacion.save()
                    return Response({'mensaje': 'Programacion desgenerada'}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'La programacion ya esta aprobada o no esta generada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumProgramacion.DoesNotExist:
            return Response({'mensaje':'La programacion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)               
        
    @action(detail=False, methods=["post"], url_path=r'aprobar',)
    def aprobar(self, request):             
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                programacion = HumProgramacion.objects.get(pk=id)
                if programacion.estado_generado == True and programacion.estado_aprobado == False:
                    documento_tipo = GenDocumentoTipo.objects.get(pk=14)                    
                    programacion_detalles = HumProgramacionDetalle.objects.filter(programacion_id=id)                    
                    inconsistencias = []
                    if not programacion_detalles:
                        inconsistencia = {
                            'descripcion': "La programacion no tiene detalles"
                        }
                        inconsistencias.append(inconsistencia)
                    for programacion_detalle in programacion_detalles:
                        if programacion_detalle.error_terminacion:
                            inconsistencia = {
                                'descripcion': "El contrato tiene fecha de terminacion anterior a la programacion y no esta terminado"
                            }
                            inconsistencias.append(inconsistencia)
                    if not inconsistencias:
                        for programacion_detalle in programacion_detalles:
                            if programacion_detalle.total < 0:
                                return Response({'mensaje':'La programacion tiene detalles negativos', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                            
                            documentos = GenDocumento.objects.filter(programacion_detalle_id=programacion_detalle.id)
                            for documento in documentos:
                                documento.numero = documento_tipo.consecutivo
                                documento.estado_aprobado = True
                                documento.pendiente = documento.total 
                                documento.save()
                                documento_tipo.consecutivo += 1

                                # Afectar creditos
                                documentos_detalles = GenDocumentoDetalle.objects.filter(documento_id=documento.id)
                                for documento_detalle in documentos_detalles:
                                    if documento_detalle.credito:
                                        credito = documento_detalle.credito
                                        credito.abono += documento_detalle.pago
                                        credito.saldo -= documento_detalle.pago
                                        credito.cuota_actual += 1
                                        credito.save()

                            # Afectar contratos
                            contrato = programacion_detalle.contrato
                            if programacion.pago_tipo_id == 1:
                                contrato.fecha_ultimo_pago = programacion.fecha_hasta
                            if programacion.pago_tipo_id == 2:
                                contrato.fecha_ultimo_pago_prima = programacion.fecha_hasta
                            if programacion.pago_tipo_id == 3:
                                contrato.fecha_ultimo_pago_cesantia = programacion.fecha_hasta
                            contrato.save()                        

                        # Para guardar el consecutivo que sigue
                        documento_tipo.save()
                        programacion.estado_aprobado = True
                        programacion.save()
                        return Response({'mensaje': 'Programacion aprobada'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'mensaje':'Se presentaron inconsistencias', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje':'La programacion ya esta aprobada o no esta generada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumProgramacion.DoesNotExist:
            return Response({'mensaje':'La programacion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)  

    @action(detail=False, methods=["post"], url_path=r'desaprobar',)
    def desaprobar(self, request):             
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                programacion = HumProgramacion.objects.get(pk=id)
                if programacion.estado_aprobado == True:                                                                                                                
                    documentos = GenDocumento.objects.filter(programacion_detalle__programacion_id=id)
                    #Validar
                    for documento in documentos:
                        if documento.afectado > 0:
                            return Response({'mensaje':f'El documento {documento.id} ya tiene un egreso, no se puede desaprobar la programacion', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 
                        if documento.estado_contabilizado:
                            return Response({'mensaje':f'El documento {documento.id} ya esta contabilizado, no se puede desaprobar la programacion', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 
                    for documento in documentos:
                        documento.estado_aprobado = False
                        documento.pendiente = documento.total 
                        documento.save()                        

                        # Desafectar creditos
                        documentos_detalles = GenDocumentoDetalle.objects.filter(documento_id=documento.id)
                        for documento_detalle in documentos_detalles:
                            if documento_detalle.credito:
                                credito = documento_detalle.credito
                                credito.abono -= documento_detalle.pago
                                credito.saldo += documento_detalle.pago
                                credito.cuota_actual -= 1
                                credito.save()

                        # Desafectar contratos
                        contrato = documento.contrato
                        if programacion.pago_tipo_id == 1:
                            contrato.fecha_ultimo_pago = programacion.fecha_desde
                        if programacion.pago_tipo_id == 2:
                            contrato.fecha_ultimo_pago_prima = programacion.fecha_desde
                        if programacion.pago_tipo_id == 3:
                            contrato.fecha_ultimo_pago_cesantia = programacion.fecha_desde
                        contrato.save()                        
                    programacion.estado_aprobado = False
                    programacion.save()
                    return Response({'mensaje': 'Programacion desaprobada'}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'La programacion no esta aprobada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumProgramacion.DoesNotExist:
            return Response({'mensaje':'La programacion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=False, methods=["post"], url_path=r'imprimir',)
    def imprimir(self, request):
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                pdf = None                
                programacion = HumProgramacion.objects.get(pk=id)                            
                formato = FormatoProgramacion()
                pdf = formato.generar_pdf(id)              
                nombre_archivo = f"programacion_{id}.pdf"       
                
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
                return response
            except GenDocumento.DoesNotExist:
                return Response({'mensaje':'La programacion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)  

    @action(detail=False, methods=["post"], url_path=r'notificar',)
    def notificar(self, request):
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                programacion = HumProgramacion.objects.get(pk=id)                
                if programacion.estado_aprobado:
                    nominas = GenDocumento.objects.filter(programacion_detalle__programacion_id=id)
                    for nomina in nominas:
                        if nomina.contacto:
                            if nomina.contacto.correo:
                                if Utilidades.correo_valido(nomina.contacto.correo):
                                    formato = FormatoNomina()
                                    pdf_bytes = formato.generar_pdf(nomina.id)                             
                                    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')                    
                                    archivos = [{
                                        'B64': pdf_base64,
                                        'NombreArchivo': f"nomina_{nomina.id}.pdf"
                                    }]
                                    contenido_html = render_to_string('nomina_notificar.html', {
                                        'contacto': nomina.contacto.nombre_corto
                                    })                    
                                    correo = Zinc()  
                                    correo.correo_reddoc_v2(nomina.contacto.correo, 'Notificacion nomina', contenido_html, archivos)                 
                    return Response({'mensaje': 'Programacion notificada'}, status=status.HTTP_200_OK)
                    #return HttpResponse(contenido_html, content_type="text/html")
                else:
                    return Response({'mensaje':'La programacion no esta aprobada', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
            except HumProgramacion.DoesNotExist:
                return Response({'mensaje':'La programacion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                     
        
    @action(detail=False, methods=['post'], url_path=r'importar_horas',)
    def importar_horas(self, request):
        raw = request.data        
        archivo_base64 = raw.get('archivo_base64')
        programacion_id = raw.get('programacion_id')
        if archivo_base64:
            try:
                archivo_data = base64.b64decode(archivo_base64)
                archivo = BytesIO(archivo_data)
                wb = openpyxl.load_workbook(archivo)
                sheet = wb.active    
            except Exception as e:     
                return Response({f'mensaje':'Error procesando el archivo, valide que es un archivo de excel .xlsx', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)  
            
            data_modelo = []
            errores = False
            errores_datos = []
            registros_actualizados = 0
            for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                data = {
                    'id': row[0],
                    'contrato_id': row[1],
                    'contrato_contacto_numero_identificacion': row[2],
                    'contrato_contacto_nombre_corto': row[3],
                    'diurna': row[4],
                    'nocturna':row[5],
                    'festiva_diurna': row[6],
                    'festiva_nocturna': row[7],
                    'extra_diurna': row[8],
                    'extra_nocturna': row[9],
                    'extra_festiva_diurna': row[10],
                    'extra_festiva_nocturna': row[11],
                    'recargo_nocturno': row[12],
                    'recargo_festivo_diurno': row[13],
                    'recargo_festivo_nocturno': row[14],
                }  

                registro = HumProgramacionDetalle.objects.filter(id=data['id'], programacion_id=programacion_id).first()
                if not registro:
                    errores = True
                    error_dato = {
                        'fila': i,
                        'errores': {
                            'programacion_id': [
                                f"El registro con ID {data['id']} no pertenece a la programación con ID {programacion_id}."
                            ]
                        }
                    }
                    errores_datos.append(error_dato)
                    continue

                serializer = HumProgramacionDetalleImportarHorasSerializador(data=data)
                if serializer.is_valid():
                    validated_data = serializer.validated_data
                    validated_data['id'] = data.get('id')
                    data_modelo.append(serializer.validated_data)
                    registros_actualizados += 1
                else:
                    errores = True
                    error_dato = {
                        'fila': i,
                        'errores': serializer.errors
                    }                                    
                    errores_datos.append(error_dato)                                         
            if not errores:
                for detalle in data_modelo:
                    HumProgramacionDetalle.objects.filter(id=detalle.get('id')).update(
                        diurna=detalle['diurna'],
                        nocturna=detalle['nocturna'],
                        festiva_diurna=detalle['festiva_diurna'],
                        festiva_nocturna=detalle['festiva_nocturna'],
                        extra_diurna=detalle['extra_diurna'],
                        extra_nocturna=detalle['extra_nocturna'],
                        extra_festiva_diurna=detalle['extra_festiva_diurna'],
                        extra_festiva_nocturna=detalle['extra_festiva_nocturna'],
                        recargo_nocturno=detalle['recargo_nocturno'],
                        recargo_festivo_diurno=detalle['recargo_festivo_diurno'],
                        recargo_festivo_nocturno=detalle['recargo_festivo_nocturno'],
                    )
                return Response({'mensaje': 'Registros actualizados exitosamente', 'registros_importados': registros_actualizados}, status=status.HTTP_200_OK)
            else:
                return Response({'Mensaje': 'Errores de validación', 'codigo': 1 ,'errores_validador': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)     