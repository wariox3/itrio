from rest_framework import viewsets, permissions
from general.models.metodo_pago import MetodoPago
from general.serializers.metodo_pago import GenMetodoPagoSerializador

class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = GenMetodoPagoSerializador
    permission_classes = [permissions.IsAuthenticated]