from general.models.cuenta_banco_clase import GenCuentaBancoClase
from rest_framework import serializers

class GenCuentaBancoClaseSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = GenCuentaBancoClase
        fields = ['id', 'nombre']

