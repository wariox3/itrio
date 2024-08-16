from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.programacion import HumProgramacion
from humano.models.programacion_detalle import HumProgramacionDetalle
from humano.models.contrato import HumContrato
from humano.models.concepto_nomina import HumConceptoNomina
from general.models.documento import GenDocumento
from general.models.configuracion import GenConfiguracion
from humano.serializers.programacion import HumProgramacionSerializador
from humano.serializers.programacion_detalle import HumProgramacionDetalleSerializador
from general.serializers.documento import GenDocumentoSerializador
from general.serializers.documento_detalle import GenDocumentoDetalleSerializador
from django.db.models import Q

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


class HumProgramacionViewSet(viewsets.ModelViewSet):
    queryset = HumProgramacion.objects.all()
    serializer_class = HumProgramacionSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'cargar-contrato',)
    def cargar_contrato(self, request):
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                configuracion = GenConfiguracion.objects.filter(pk=1).values('hum_factor')[0]
                programacion = HumProgramacion.objects.get(pk=id)                                
                contratos = HumContrato.objects.filter(
                        grupo_id=programacion.grupo_id                        
                        ).filter(
                            Q(fecha_ultimo_pago__isnull=True) | Q(fecha_ultimo_pago__lt=programacion.fecha_hasta) | Q(fecha_desde=programacion.fecha_hasta_periodo) | Q(fecha_desde=programacion.fecha_hasta)
                        ).filter(
                            fecha_desde__lte=programacion.fecha_hasta_periodo
                        ).filter(
                            Q(fecha_hasta__gte=programacion.fecha_desde) | Q(contrato_tipo_id=1))                                             
                for contrato in contratos:
                    ingreso = False
                    if contrato.fecha_desde >= programacion.fecha_hasta and contrato.fecha_desde <= programacion.fecha_hasta_periodo:
                        ingreso = True                

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
                        'descuento_adicional_permanente': programacion.descuento_adicional_permanente,
                        'descuento_adicional_programacion': programacion.descuento_adicional_programacion,
                        'descuento_credito': programacion.descuento_credito,
                        'descuento_embargo': programacion.descuento_embargo,
                        'ingreso': ingreso
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
                        fecha_hasta = programacion.fecha_hasta_periodo
                    if fecha_hasta > programacion.fecha_hasta_periodo:
                        fecha_hasta = programacion.fecha_hasta_periodo
                    data['fecha_hasta'] = fecha_hasta
                    
                    diferencia = fecha_hasta - fecha_desde
                    dias = diferencia.days + 1
                    data['dias'] = dias
                    data['dias_transporte'] = dias
                    data['diurna'] = dias * configuracion['hum_factor']
                    programacion_detalle_serializador = HumProgramacionDetalleSerializador(data=data)
                    if programacion_detalle_serializador.is_valid():
                        programacion_detalle_serializador.save()
                    else:
                        return Response({'validaciones':programacion_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                    
                return Response({'contratos_cargados': True}, status=status.HTTP_200_OK)
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
                conceptos_nomina = HumConceptoNomina.objects.all().order_by('id')
                configuracion = GenConfiguracion.objects.filter(pk=1).values('hum_factor')[0]
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
                        'salario': programacion_detalle.salario                      
                    }
                    documento_serializador = GenDocumentoSerializador(data=data)
                    if documento_serializador.is_valid():
                        documento = documento_serializador.save()
                        # Variables generales
                        valor_dia_contrato = programacion_detalle.salario / 30
                        valor_hora_contrato = valor_dia_contrato / configuracion['hum_factor']
                        #valor_hora_contrato = f"{valor_hora_contrato:20.6f}"


                        horas = horas_programacion(programacion_detalle)
                        for hora in horas:
                            if hora['cantidad'] > 0:
                                concepto_nomina = conceptos_nomina[hora['clave']] 
                                concepto = concepto_nomina.concepto                                
                                #valor_hora_detalle = f"{valor_hora_contrato:20.6f}"
                                valor_hora_detalle = (valor_hora_contrato * concepto.porcentaje) / 100                                
                                pago = valor_hora_detalle * hora['cantidad']
                                data = {
                                    'documento': documento.id,
                                    'cantidad': hora['cantidad'],                   
                                    'hora': f"{valor_hora_detalle:20.6f}",
                                    'porcentaje': concepto.porcentaje,
                                    'pago': f"{pago:20.6f}",
                                    'concepto': concepto_nomina.concepto_id
                                }
                                documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                                if documento_detalle_serializador.is_valid():
                                    documento_detalle_serializador.save()
                                else:
                                    return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                                
                    else:
                        return Response({'validaciones':documento_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                    
                return Response({'contratos_cargados': True}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumProgramacion.DoesNotExist:
            return Response({'mensaje':'La programacion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)             