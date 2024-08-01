from rest_framework import viewsets, permissions
from general.models.precio import Precio
from general.serializers.precio import GenPrecioSerializador

class PrecioViewSet(viewsets.ModelViewSet):
    queryset = Precio.objects.all()
    serializer_class = GenPrecioSerializador
    permission_classes = [permissions.IsAuthenticated]