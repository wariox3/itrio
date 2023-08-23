from rest_framework import viewsets, permissions
from general.models.tipo_persona import TipoPersona
from general.serializers.tipo_persona import TipoPersonaSerializador

class TipoPersonaViewSet(viewsets.ModelViewSet):
    queryset = TipoPersona.objects.all()
    serializer_class = TipoPersonaSerializador
    permission_classes = [permissions.IsAuthenticated]