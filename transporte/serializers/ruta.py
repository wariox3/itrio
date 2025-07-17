from rest_framework import serializers
from transporte.models.ruta import TteRuta

class TteRutaSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteRuta
        fields = ['id', 'nombre']

class TteRutaSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteRuta
        fields = ['id', 'nombre']
