from rest_framework import viewsets, permissions
from contabilidad.models.con_comprobante import ConComprobante
from contabilidad.serializers.comprobante import ConComprobanteSerializador

class ComprobanteViewSet(viewsets.ModelViewSet):
    queryset = ConComprobante.objects.all()
    serializer_class = ConComprobanteSerializador
    permission_classes = [permissions.IsAuthenticated]