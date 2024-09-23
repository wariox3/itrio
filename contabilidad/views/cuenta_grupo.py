from rest_framework import viewsets, permissions
from contabilidad.models.cuenta_grupo import ConCuentaGrupo
from contabilidad.serializers.cuenta_grupo import ConCuentaGrupoSerializador

class CuentaGrupoViewSet(viewsets.ModelViewSet):
    queryset = ConCuentaGrupo.objects.all()
    serializer_class = ConCuentaGrupoSerializador
    permission_classes = [permissions.IsAuthenticated]