from rest_framework import serializers
from transporte.models.combustible import TteCombustible

class TteCombustibleSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteCombustible
        fields = ['id', 'nombre']

class TteCombustibleSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteCombustible
        fields = ['id', 'nombre']
