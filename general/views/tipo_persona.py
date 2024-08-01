from rest_framework import viewsets, permissions
from general.models.tipo_persona import TipoPersona
from general.serializers.tipo_persona import GenTipoPersonaSerializador

class TipoPersonaViewSet(viewsets.ModelViewSet):
    queryset = TipoPersona.objects.all()
    serializer_class = GenTipoPersonaSerializador
    permission_classes = [permissions.IsAuthenticated]