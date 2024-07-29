from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from humano.models.hum_programacion import HumProgramacion
from humano.models.hum_programacion_detalle import HumProgramacionDetalle
from humano.models.hum_contrato import HumContrato
from humano.serializers.hum_programacion import HumProgramacionSerializador
from humano.serializers.hum_contrato import HumContratoSerializador
from humano.filters.hum_programacion import HumProgramacionFilter

class HumProgramacionViewSet(viewsets.ModelViewSet):
    queryset = HumProgramacion.objects.all()
    serializer_class = HumProgramacionSerializador
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = HumProgramacionFilter
    ordering_fields = ['id']
    ordering = ['id']    


    @action(detail=False, methods=["post"], url_path=r'cargar-contrato',)
    def cargar_contrato(self, request):
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                programacion = HumProgramacion.objects.get(pk=id)
                contratos = HumContrato.objects.all()
                for contrato in contratos:
                    programacion_detalle = HumProgramacionDetalle(
                        programacion=programacion,
                        contrato=contrato
                    )
                programacion_detalle.save()
                return Response({'contratos_cargados': True}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumProgramacion.DoesNotExist:
            return Response({'mensaje':'La programacion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)    