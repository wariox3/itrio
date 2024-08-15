from rest_framework import viewsets, permissions
from humano.models.salud import HumSalud
from humano.serializers.salud import HumSaludSerializador

class HumSaludViewSet(viewsets.ModelViewSet):
    queryset = HumSalud.objects.all()
    serializer_class = HumSaludSerializador
    permission_classes = [permissions.IsAuthenticated]