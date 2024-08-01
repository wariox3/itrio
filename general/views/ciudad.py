from rest_framework import viewsets, permissions
from general.models.ciudad import Ciudad
from general.serializers.ciudad import GenCiudadSerializador

class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = GenCiudadSerializador
    permission_classes = [permissions.IsAuthenticated]