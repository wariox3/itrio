from rest_framework import viewsets, permissions
from general.models.tipo_persona import GenTipoPersona
from general.serializers.tipo_persona import GenTipoPersonaSerializador

class TipoPersonaViewSet(viewsets.ModelViewSet):
    queryset = GenTipoPersona.objects.all()
    serializer_class = GenTipoPersonaSerializador
    permission_classes = [permissions.IsAuthenticated]