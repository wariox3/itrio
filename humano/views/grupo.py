from rest_framework import viewsets, permissions
from humano.models.grupo import HumGrupo
from humano.serializers.grupo import HumGrupoSerializador

class HumGrupoViewSet(viewsets.ModelViewSet):
    queryset = HumGrupo.objects.all()
    serializer_class = HumGrupoSerializador
    permission_classes = [permissions.IsAuthenticated]