from rest_framework import viewsets, permissions
from inventario.models.almacen import InvAlmacen
from inventario.serializers.almacen import InvAlmacenSerializador

class InvAlmacenViewSet(viewsets.ModelViewSet):
    queryset = InvAlmacen.objects.all()
    serializer_class = InvAlmacenSerializador
    permission_classes = [permissions.IsAuthenticated]