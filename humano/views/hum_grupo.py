from rest_framework import viewsets, permissions
from humano.models.hum_grupo import HumGrupo
from humano.serializers.hum_grupo import HumGrupoSerializador

class HumGrupoViewSet(viewsets.ModelViewSet):
    queryset = HumGrupo.objects.all()
    serializer_class = HumGrupoSerializador
    permission_classes = [permissions.IsAuthenticated]