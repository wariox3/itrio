from rest_framework import viewsets, permissions
from general.models.plazo_pago import PlazoPago
from general.serializers.plazo_pago import PlazoPagoSerializador
from rest_framework.decorators import action
from rest_framework.response import Response

class PlazoPagoViewSet(viewsets.ModelViewSet):
    queryset = PlazoPago.objects.all()
    serializer_class = PlazoPagoSerializador    
    permission_classes = [permissions.IsAuthenticated]        