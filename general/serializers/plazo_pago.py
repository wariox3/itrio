from general.models.plazo_pago import GenPlazoPago
from rest_framework import serializers

class GenPlazoPagoSerializador(serializers.ModelSerializer):
    class Meta:
        model = GenPlazoPago
        fields = ['id', 'nombre', 'dias'] 