from rest_framework import viewsets, permissions
from humano.models.novedad import HumNovedad
from humano.serializers.novedad import HumNovedadSerializador

class HumNovedadViewSet(viewsets.ModelViewSet):
    queryset = HumNovedad.objects.all()
    serializer_class = HumNovedadSerializador
    permission_classes = [permissions.IsAuthenticated]