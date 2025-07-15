from rest_framework import serializers
from transporte.models.color import TteColor

class TteColorSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteColor
        fields = ['id', 'nombre']

class TteColorSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteColor
        fields = ['id', 'nombre']
