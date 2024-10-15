from rest_framework import viewsets, permissions
from humano.models.aporte import HumAporte
from humano.serializers.aporte import HumAporteSerializador

class HumAporteViewSet(viewsets.ModelViewSet):
    queryset = HumAporte.objects.all()
    serializer_class = HumAporteSerializador
    permission_classes = [permissions.IsAuthenticated]      