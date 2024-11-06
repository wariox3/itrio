from rest_framework import viewsets, permissions
from humano.models.aporte_contrato import HumAporteContrato
from humano.serializers.aporte_contrato import HumAporteContratoSerializador

class HumAporteContratoViewSet(viewsets.ModelViewSet):
    queryset = HumAporteContrato.objects.all()
    serializer_class = HumAporteContratoSerializador
    permission_classes = [permissions.IsAuthenticated]      