from rest_framework import viewsets, permissions
from general.models.plazo_pago import PlazoPago
from general.serializers.plazo_pago import PlazoPagoSerializador

class PlazoPagoViewSet(viewsets.ModelViewSet):
    queryset = PlazoPago.objects.all()
    serializer_class = PlazoPagoSerializador    
    permission_classes = [permissions.IsAuthenticated]               