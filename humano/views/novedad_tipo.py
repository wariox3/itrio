from rest_framework import viewsets, permissions
from humano.models.novedad_tipo import HumNovedadTipo
from humano.serializers.novedad_tipo import HumNovedadTipoSerializador

class HumNovedadTipoViewSet(viewsets.ModelViewSet):
    queryset = HumNovedadTipo.objects.all()
    serializer_class = HumNovedadTipoSerializador
    permission_classes = [permissions.IsAuthenticated]