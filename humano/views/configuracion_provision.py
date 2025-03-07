from rest_framework import viewsets, permissions
from humano.models.configuracion_provision import HumConfiguracionProvision
from humano.serializers.configuracion_provision import HumConfiguracionProvisionSerializador

class HumConfiguracionProvisionViewSet(viewsets.ModelViewSet):
    queryset = HumConfiguracionProvision.objects.all()
    serializer_class = HumConfiguracionProvisionSerializador
    permission_classes = [permissions.IsAuthenticated]