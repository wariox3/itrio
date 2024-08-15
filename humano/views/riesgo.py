from rest_framework import viewsets, permissions
from humano.models.riesgo import HumRiesgo
from humano.serializers.riesgo import HumRiesgoSerializador

class HumRiesgoViewSet(viewsets.ModelViewSet):
    queryset = HumRiesgo.objects.all()
    serializer_class = HumRiesgoSerializador
    permission_classes = [permissions.IsAuthenticated]