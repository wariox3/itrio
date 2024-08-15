from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.programacion import HumProgramacion
from humano.models.contrato import HumContrato
from humano.serializers.programacion import HumProgramacionSerializador
from humano.serializers.programacion_detalle import HumProgramacionDetalleSerializador
from django.db.models import Q
from datetime import date

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
                programacion = HumProgramacion.objects.get(pk=id)
                
                contratos = HumContrato.objects.filter(
                        grupo_id=programacion.grupo_id                        
                        ).filter(
                            Q(fecha_ultimo_pago__lt=programacion.fecha_hasta) | Q(fecha_desde=programacion.fecha_hasta_periodo) | Q(fecha_desde=programacion.fecha_hasta)
                        ).filter(
                            fecha_desde__lte=programacion.fecha_hasta_periodo
                        ).filter(
                            Q(fecha_hasta__gte=programacion.fecha_desde) | Q(contrato_tipo_id=1))                
                #contratos = HumContrato.objects.all()
                for contrato in contratos:
                    ingreso = False
                    if contrato.fecha_desde >= programacion.fecha_hasta and contrato.fecha_desde <= programacion.fecha_hasta_periodo:
                        ingreso = True                

                    data = {
                        'programacion': programacion.id,
                        'contrato': contrato.id,
                        'fecha_desde': programacion.fecha_desde,
                        'fecha_hasta': programacion.fecha_hasta,
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
            
                    '''if ($arContrato->getCodigoPensionFk() == 'PEN') {
                        $arProgramacionDetalle->setDescuentoPension(0);
                    }'''
                        
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
        return Response({'mensaje': 'Programacion generada con exito'}, status=status.HTTP_200_OK)        