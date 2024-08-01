from rest_framework import viewsets, permissions
from general.models.plazo_pago import GenPlazoPago
from general.serializers.plazo_pago import GenPlazoPagoSerializador
from rest_framework.decorators import action
from rest_framework.response import Response

class PlazoPagoViewSet(viewsets.ModelViewSet):
    queryset = GenPlazoPago.objects.all()
    serializer_class = GenPlazoPagoSerializador    
    permission_classes = [permissions.IsAuthenticated]        