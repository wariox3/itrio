from rest_framework import viewsets, permissions
from general.models.ciudad import GenCiudad
from general.serializers.ciudad import GenCiudadSerializador

class CiudadViewSet(viewsets.ModelViewSet):
    queryset = GenCiudad.objects.all()
    serializer_class = GenCiudadSerializador
    permission_classes = [permissions.IsAuthenticated]