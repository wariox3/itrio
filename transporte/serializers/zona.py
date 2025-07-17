from rest_framework import serializers
from transporte.models.zona import TteZona

class TteZonaSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteZona
        fields = ['id', 'nombre']

class TteZonaSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteZona
        fields = ['id', 'nombre']
