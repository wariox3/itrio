from rest_framework import viewsets, permissions
from humano.models.hum_contrato import HumContrato
from humano.serializers.hum_contrato import HumContratoSerializador

class HumMovimientoViewSet(viewsets.ModelViewSet):
    queryset = HumContrato.objects.all()
    serializer_class = HumContratoSerializador
    permission_classes = [permissions.IsAuthenticated]