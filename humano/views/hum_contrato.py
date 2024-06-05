from rest_framework import viewsets, permissions
from humano.models.hum_contrato import HumContrato
from humano.serializers.hum_contrato import HumContratoSerializer

class HumMovimientoViewSet(viewsets.ModelViewSet):
    queryset = HumContrato.objects.all()
    serializer_class = HumContratoSerializer
    permission_classes = [permissions.IsAuthenticated]