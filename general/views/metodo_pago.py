from rest_framework import viewsets, permissions
from general.models.metodo_pago import MetodoPago
from general.serializers.metodo_pago import MetodoPagoSerializador

class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializador
    permission_classes = [permissions.IsAuthenticated]