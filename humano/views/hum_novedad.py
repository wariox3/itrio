from rest_framework import viewsets, permissions
from humano.models.hum_novedad import HumNovedad
from humano.serializers.hum_novedad import HumNovedadSerializador

class HumNovedadViewSet(viewsets.ModelViewSet):
    queryset = HumNovedad.objects.all()
    serializer_class = HumNovedadSerializador
    permission_classes = [permissions.IsAuthenticated]