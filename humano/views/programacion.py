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
from humano.serializers.programacion import HumProgramacionSerializador
from humano.serializers.programacion_detalle import HumProgramacionDetalleSerializador
from general.serializers.documento import GenDocumentoSerializador
from general.serializers.documento_detalle import GenDocumentoDetalleSerializador
from general.formatos.programacion import FormatoProgramacion
from general.formatos.nomina import FormatoNomina
from django.db.models import Q
from django.http import HttpResponse
from decimal import Decimal, ROUND_HALF_UP
from datetime import timedelta
import calendar
from django.template.loader import render_to_string
from utilidades.zinc import Zinc
from utilidades.utilidades import Utilidades
import base64

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
    return data

class HumProgramacionViewSet(viewsets.ModelViewSet):
    queryset = HumProgramacion.objects.all()
    serializer_class = HumProgramacionSerializador
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        fecha_desde = serializer.validated_data.get('fecha_desde')
        fecha_hasta = serializer.validated_data.get('fecha_hasta')
        fecha_hasta_periodo = serializer.validated_data.get('fecha_hasta')
        diferencia = fecha_hasta - fecha_desde
        dias = diferencia.days + 1      
                
        if fecha_hasta.day == 30: 
            ultimo_dia = calendar.monthrange(fecha_hasta.year, fecha_hasta.month)[1]       
            if ultimo_dia == 31:
                fecha_hasta_periodo = fecha_hasta + timedelta(days=1)
        serializer.save(dias=dias, fecha_hasta_periodo=fecha_hasta_periodo)

    def perform_update(self, serializer):
        fecha_desde = serializer.validated_data.get('fecha_desde')
        fecha_hasta = serializer.validated_data.get('fecha_hasta')
        fecha_hasta_periodo = serializer.validated_data.get('fecha_hasta')
        diferencia = fecha_hasta - fecha_desde
        dias = diferencia.days + 1      
                
        if fecha_hasta.day == 30: 
            ultimo_dia = calendar.monthrange(fecha_hasta.year, fecha_hasta.month)[1]       
            if ultimo_dia == 31:
                fecha_hasta_periodo = fecha_hasta + timedelta(days=1)
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
                    cantidad = programacion.contratos
                    configuracion = GenConfiguracion.objects.filter(pk=1).values('hum_factor', 'hum_auxilio_transporte')[0]                
                    if programacion.pago_tipo_id == 1:
                        contratos = HumContrato.objects.filter(
                                grupo_id=programacion.grupo_id                        
                                ).filter(
                                    Q(fecha_ultimo_pago__isnull=True) | Q(fecha_ultimo_pago__lt=programacion.fecha_hasta) | Q(fecha_desde=programacion.fecha_hasta_periodo) | Q(fecha_desde=programacion.fecha_hasta)
                                ).filter(
                                    fecha_desde__lte=programacion.fecha_hasta_periodo
                                ).filter(
                                    Q(fecha_hasta__gte=programacion.fecha_desde) | Q(contrato_tipo_id=1))                                             
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
                                    'retiro': retiro
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
                                    
                                fecha_hasta = contrato.fecha_hasta
                                if contrato.contrato_tipo_id == 1:
                                    fecha_hasta = programacion.fecha_hasta
                                if fecha_hasta > programacion.fecha_hasta:
                                    fecha_hasta = programacion.fecha_hasta
                                data['fecha_hasta'] = fecha_hasta
                                
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
                                data['dias'] = dias
                                data['dias_transporte'] = dias
                                data['dias_novedad'] = dias_novedad
                                data['diurna'] = dias * configuracion['hum_factor']
                                programacion_detalle_serializador = HumProgramacionDetalleSerializador(data=data)
                                if programacion_detalle_serializador.is_valid():
                                    programacion_detalle_serializador.save()
                                    cantidad += 1
                                else:
                                    return Response({'validaciones':programacion_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)
                    
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
                    total_programacion = 0
                    devengado_programacion = 0
                    deduccion_programacion = 0
                    conceptos_nomina = HumConceptoNomina.objects.all().order_by('id')
                    configuracion = GenConfiguracion.objects.filter(pk=1).values('hum_factor', 'hum_auxilio_transporte')[0]
                    programacion_detalles = HumProgramacionDetalle.objects.filter(programacion_id=id)                                           
                    for programacion_detalle in programacion_detalles:                                  
                        data = {
                            'programacion_detalle': programacion_detalle.id,
                            'documento_tipo': 14,
                            'empresa': 1,
                            'fecha': programacion_detalle.fecha_desde,
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
                            contrato = programacion_detalle.contrato
                            valor_dia_contrato = programacion_detalle.salario / 30
                            valor_hora_contrato = valor_dia_contrato / configuracion['hum_factor']
                                                       
                            data_general = {
                                'devengado': 0,
                                'deduccion': 0,
                                'base_cotizacion': 0,
                                'base_prestacion': 0,
                                'base_licencia': 0,
                            }
                            #Nomina
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
                                            data = {
                                                'documento': documento.id,
                                                'cantidad': hora['cantidad'],                   
                                                'hora': valor_hora_detalle, 
                                                'dias': programacion_detalle.dias,
                                                'porcentaje': concepto.porcentaje,
                                                'pago': pago,
                                                'concepto': concepto_nomina.concepto_id
                                            }
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
                                                    data = {
                                                        'documento': documento.id,  
                                                        'dias': dias_empresa,
                                                        'hora': novedad.hora_empresa,
                                                        'cantidad': horas,
                                                        'pago': pago,
                                                        'porcentaje': concepto.porcentaje,
                                                        'concepto': novedad.novedad_tipo.concepto_id
                                                    }
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
                                                    data = {
                                                        'documento': documento.id,  
                                                        'dias': dias_entidad,
                                                        'hora': novedad.hora_entidad,
                                                        'cantidad': horas,
                                                        'pago': pago,
                                                        'porcentaje': concepto.porcentaje,
                                                        'concepto': novedad.novedad_tipo.concepto2_id
                                                    }
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
                                                data = {
                                                    'documento': documento.id,  
                                                    'dias': dias_novedad,
                                                    'hora': hora,
                                                    'cantidad': horas,
                                                    'pago': pago,
                                                    'porcentaje': concepto.porcentaje,
                                                    'concepto': novedad.novedad_tipo.concepto_id
                                                }
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
                                            data = {
                                                'documento': documento.id,  
                                                'dias': dias_novedad,
                                                'pago': pago,
                                                'concepto': novedad.novedad_tipo.concepto_id
                                            }
                                            data = datos_detalle(data_general, data, concepto)
                                            documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                            if documento_detalle_serializador.is_valid():
                                                documento_detalle_serializador.save()
                                            else:
                                                return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)  

                                            # Vacaciones en dinero
                                            concepto = novedad.novedad_tipo.concepto2
                                            pago = round(dias_novedad_pago * novedad.pago_dia_dinero)                                    
                                            data = {
                                                'documento': documento.id,  
                                                'dias': dias_novedad,
                                                'pago': pago,
                                                'concepto': novedad.novedad_tipo.concepto2_id
                                            }
                                            data = datos_detalle(data_general, data, concepto)
                                            documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                            if documento_detalle_serializador.is_valid():
                                                documento_detalle_serializador.save()
                                            else:
                                                return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                                                           

                                # Adicionales
                                if programacion_detalle.adicional:
                                    adicionales = HumAdicional.objects.filter(
                                            inactivo = False, 
                                            inactivo_periodo = False,
                                            contrato_id = programacion_detalle.contrato_id
                                        ).filter(
                                            Q(permanente=True) | Q(programacion_id=programacion.id)
                                        )
                                    for adicional in adicionales:                        
                                        concepto = adicional.concepto
                                        data = {
                                            'documento': documento.id,                                                                                                                
                                            'pago': round(adicional.valor),
                                            'concepto': adicional.concepto_id
                                        }
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
                                            data = {
                                                'documento': documento.id,                                                                                    
                                                'pago': pago,
                                                'dias': programacion_detalle.dias_transporte,
                                                'concepto': concepto.id
                                            }
                                            datos_detalle(data_general, data, concepto)
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
                                            base = data_general['base_cotizacion'] - data_general['base_licencia'];                                  
                                            pago = round((base * salud.porcentaje_empleado) / 100)
                                            data = {
                                                'documento': documento.id,                                            
                                                'porcentaje': salud.porcentaje_empleado,
                                                'pago': pago,
                                                'concepto': concepto.id
                                            }
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
                                            concepto = pension.concepto                                        
                                            pago = round((data_general['base_cotizacion'] * pension.porcentaje_empleado) / 100)                                        
                                            data = {
                                                'documento': documento.id,                                            
                                                'porcentaje': pension.porcentaje_empleado,
                                                'pago': pago,
                                                'concepto': concepto.id
                                            }
                                            datos_detalle(data_general, data, concepto)
                                            documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                            if documento_detalle_serializador.is_valid():
                                                documento_detalle_serializador.save()
                                            else:
                                                return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)

                                #creditos
                                if programacion_detalle.descuento_credito:
                                    creditos = HumCredito.objects.filter(
                                            inactivo = False, 
                                            inactivo_periodo = False,
                                            pagado = False,
                                            contrato_id = programacion_detalle.contrato_id
                                        )
                                    for credito in creditos: 
                                        if credito.saldo > 0:                       
                                            concepto = credito.concepto
                                            if credito.saldo >= credito.cuota:
                                                pago = credito.cuota
                                            else:
                                                pago = credito.saldo;                                                                                                
                                            data = {
                                                'documento': documento.id,                                                                                                                
                                                'pago': round(pago),
                                                'concepto': credito.concepto_id,
                                                'credito': credito.id
                                            }
                                            data = datos_detalle(data_general, data, concepto)
                                            documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                            if documento_detalle_serializador.is_valid():
                                                documento_detalle_serializador.save()
                                            else:
                                                return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                
                            
                            #prima
                            if programacion.pago_tipo_id == 2:
                                prima = (programacion_detalle.salario_promedio * programacion_detalle.dias) / 360
                                concepto_nomina = conceptos_nomina[12]
                                concepto = concepto_nomina.concepto
                                pago = round(prima)                                    
                                if pago > 0:
                                    data = {
                                        'documento': documento.id,                                                                                    
                                        'pago': pago,
                                        'dias': programacion_detalle.dias_transporte,
                                        'concepto': concepto.id
                                    }
                                    datos_detalle(data_general, data, concepto)
                                    documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                    if documento_detalle_serializador.is_valid():
                                        documento_detalle_serializador.save()
                                    else:
                                        return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                
                            
                            total = data_general['devengado'] - data_general['deduccion']
                            devengado = data_general['devengado']
                            deduccion = data_general['deduccion']
                            documento.base_cotizacion = data_general['base_cotizacion']
                            documento.base_prestacion = data_general['base_prestacion']
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
                        contrato.fecha_ultimo_pago = programacion.fecha_hasta
                        contrato.save()                        

                    # Para guardar el consecutivo que sigue
                    documento_tipo.save()
                    programacion.estado_aprobado = True
                    programacion.save()
                    return Response({'mensaje': 'Programacion aprobada'}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'La programacion ya esta aprobada o no esta generada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
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