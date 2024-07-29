from rest_framework import viewsets, permissions
from contabilidad.models.con_movimiento import ConMovimiento
from contabilidad.serializers.movimiento import MovimientoSerializer

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = ConMovimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [permissions.IsAuthenticated]