from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ruteo.models.novedad import RutNovedad
from ruteo.serializers.novedad import RutNovedadSerializador

class RutNovedadViewSet(viewsets.ModelViewSet):
    queryset = RutNovedad.objects.all()
    serializer_class = RutNovedadSerializador
    permission_classes = [permissions.IsAuthenticated]                 