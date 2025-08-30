from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.producto import VerProducto
from vertical.serializers.producto import VerProductoSerializador

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = VerProducto.objects.all()
    serializer_class = VerProductoSerializador
    permission_classes = [permissions.IsAuthenticated]