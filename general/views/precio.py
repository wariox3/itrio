from rest_framework import viewsets, permissions
from general.models.precio import Precio
from general.serializers.precio import PrecioSerializador

class PrecioViewSet(viewsets.ModelViewSet):
    queryset = Precio.objects.all()
    serializer_class = PrecioSerializador
    permission_classes = [permissions.IsAuthenticated]