from rest_framework import serializers
from transporte.models.linea import TteLinea

class TteLineaSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteLinea
        fields = ['id', 'nombre']

class TteLineaSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteLinea
        fields = ['id', 'nombre']
