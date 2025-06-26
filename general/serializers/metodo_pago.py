from general.models.metodo_pago import GenMetodoPago
from rest_framework import serializers

class GenMetodoPagoSerializador(serializers.ModelSerializer):
    class Meta:
        model = GenMetodoPago
        fields = ['id', 'nombre']  
         
