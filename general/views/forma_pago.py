from rest_framework import viewsets, permissions
from general.models.forma_pago import GenFormaPago
from general.serializers.forma_pago import GenFormaPagoSerializador
from rest_framework.decorators import action
from rest_framework.response import Response

class FormaPagoViewSet(viewsets.ModelViewSet):
    queryset = GenFormaPago.objects.all()
    serializer_class = GenFormaPagoSerializador    
    permission_classes = [permissions.IsAuthenticated]        