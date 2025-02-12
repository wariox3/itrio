from rest_framework import viewsets, permissions
from humano.models.tiempo import HumTiempo
from humano.serializers.tiempo import HumTiempoSerializador

class HumTiempoViewSet(viewsets.ModelViewSet):
    queryset = HumTiempo.objects.all()
    serializer_class = HumTiempoSerializador
    permission_classes = [permissions.IsAuthenticated]