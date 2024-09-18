from rest_framework import viewsets, permissions
from humano.models.periodo import HumPeriodo
from humano.serializers.periodo import HumPeriodoSerializador

class HumPeriodoViewSet(viewsets.ModelViewSet):
    queryset = HumPeriodo.objects.all()
    serializer_class = HumPeriodoSerializador
    permission_classes = [permissions.IsAuthenticated]