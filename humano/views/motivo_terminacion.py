from rest_framework import viewsets, permissions
from humano.models.motivo_terminacion import HumMotivoTerminacion
from humano.serializers.motivo_terminacion import HumMotivoTerminacionSerializador

class HumConceptoCuentaViewSet(viewsets.ModelViewSet):
    queryset = HumMotivoTerminacion.objects.all()
    serializer_class = HumMotivoTerminacionSerializador
    permission_classes = [permissions.IsAuthenticated]