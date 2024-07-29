from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from humano.models.hum_programacion import HumProgramacion
from humano.models.hum_programacion_detalle import HumProgramacionDetalle
from humano.models.hum_contrato import HumContrato
from humano.serializers.hum_programacion import HumProgramacionSerializador
from humano.serializers.hum_programacion_detalle import HumProgramacionDetalleSerializador

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
                contratos = HumContrato.objects.all()
                for contrato in contratos:
                    data = {
                        'programacion': programacion.id,
                        'contrato': contrato.id,
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
                        'descuento_embargo': programacion.descuento_embargo

                    }
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