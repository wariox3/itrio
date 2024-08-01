from rest_framework import viewsets, permissions
from general.models.plazo_pago import PlazoPago
from general.serializers.plazo_pago import GenPlazoPagoSerializador
from rest_framework.decorators import action
from rest_framework.response import Response

class PlazoPagoViewSet(viewsets.ModelViewSet):
    queryset = PlazoPago.objects.all()
    serializer_class = GenPlazoPagoSerializador    
    permission_classes = [permissions.IsAuthenticated]        