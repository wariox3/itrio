from rest_framework import viewsets, permissions
from humano.models.entidad import HumEntidad
from humano.serializers.entidad import HumEntidadSerializador

class HumEntidadViewSet(viewsets.ModelViewSet):
    queryset = HumEntidad.objects.all()
    serializer_class = HumEntidadSerializador
    permission_classes = [permissions.IsAuthenticated]