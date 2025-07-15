from rest_framework import serializers
from transporte.models.carroceria import TteCarroceria

class TteCarroceriaSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteCarroceria
        fields = ['id', 'nombre']

class TteCarroceriaSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteCarroceria
        fields = ['id', 'nombre']
