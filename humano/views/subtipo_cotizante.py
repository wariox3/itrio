from rest_framework import viewsets, permissions
from humano.models.subtipo_cotizante import HumSubtipoCotizante
from humano.serializers.subtipo_cotizante import HumSubtipoCotizanteSerializador

class HumSubtipoCotizanteViewSet(viewsets.ModelViewSet):
    queryset = HumSubtipoCotizante.objects.all()
    serializer_class = HumSubtipoCotizanteSerializador
    permission_classes = [permissions.IsAuthenticated]