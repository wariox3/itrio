from rest_framework import viewsets, permissions
from contabilidad.models.movimiento import Movimiento
from contabilidad.serializers.movimiento import MovimientoSerializer

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [permissions.IsAuthenticated]