from rest_framework import viewsets, permissions
from humano.models.configuracion_aporte import HumConfiguracionAporte
from humano.serializers.configuracion_aporte import HumConfiguracionAporteSerializador

class HumConfiguracionAporteViewSet(viewsets.ModelViewSet):
    queryset = HumConfiguracionAporte.objects.all()
    serializer_class = HumConfiguracionAporteSerializador
    permission_classes = [permissions.IsAuthenticated]