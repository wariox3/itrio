from rest_framework import viewsets, permissions
from general.models.identificacion import Identificacion
from general.serializers.identificacion import IdentificacionSerializador

class IdentificacionViewSet(viewsets.ModelViewSet):
    queryset = Identificacion.objects.all()
    serializer_class = IdentificacionSerializador
    permission_classes = [permissions.IsAuthenticated]