from rest_framework import viewsets, permissions
from general.models.precio_detalle import PrecioDetalle
from general.serializers.precio_detalle import GenPrecioDetalleSerializador

class PrecioDetalleViewSet(viewsets.ModelViewSet):
    queryset = PrecioDetalle.objects.all()
    serializer_class = GenPrecioDetalleSerializador
    permission_classes = [permissions.IsAuthenticated]