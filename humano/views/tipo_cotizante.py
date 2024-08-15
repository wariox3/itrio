from rest_framework import viewsets, permissions
from humano.models.tipo_cotizante import HumTipoCotizante
from humano.serializers.tipo_cotizante import HumTipoCotizanteSerializador

class HumTipoCotizanteViewSet(viewsets.ModelViewSet):
    queryset = HumTipoCotizante.objects.all()
    serializer_class = HumTipoCotizanteSerializador
    permission_classes = [permissions.IsAuthenticated]