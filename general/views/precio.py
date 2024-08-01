from rest_framework import viewsets, permissions
from general.models.precio import GenPrecio
from general.serializers.precio import GenPrecioSerializador

class PrecioViewSet(viewsets.ModelViewSet):
    queryset = GenPrecio.objects.all()
    serializer_class = GenPrecioSerializador
    permission_classes = [permissions.IsAuthenticated]