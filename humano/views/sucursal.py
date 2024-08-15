from rest_framework import viewsets, permissions
from humano.models.sucursal import HumSucursal
from humano.serializers.sucursal import HumSucursalSerializador

class HumSucursalViewSet(viewsets.ModelViewSet):
    queryset = HumSucursal.objects.all()
    serializer_class = HumSucursalSerializador
    permission_classes = [permissions.IsAuthenticated]