from rest_framework import viewsets, permissions
from general.models.identificacion import GenIdentificacion
from general.serializers.identificacion import GenIdentificacionSerializador

class IdentificacionViewSet(viewsets.ModelViewSet):
    queryset = GenIdentificacion.objects.all()
    serializer_class = GenIdentificacionSerializador
    permission_classes = [permissions.IsAuthenticated]