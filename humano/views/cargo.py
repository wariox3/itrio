from rest_framework import viewsets, permissions
from humano.models.cargo import HumCargo
from humano.serializers.cargo import HumCargoSerializador

class HumCargoViewSet(viewsets.ModelViewSet):
    queryset = HumCargo.objects.all()
    serializer_class = HumCargoSerializador
    permission_classes = [permissions.IsAuthenticated]