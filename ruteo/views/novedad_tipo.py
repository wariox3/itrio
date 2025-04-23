from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ruteo.models.novedad_tipo import RutNovedadTipo
from ruteo.serializers.novedad_tipo import RutNovedadTipoSerializador

class RutNovedadTipoViewSet(viewsets.ModelViewSet):
    queryset = RutNovedadTipo.objects.all()
    serializer_class = RutNovedadTipoSerializador
    permission_classes = [permissions.IsAuthenticated]                 