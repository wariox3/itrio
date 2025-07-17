from rest_framework import serializers
from transporte.models.operacion import TteOperacion

class TteOperacionSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteOperacion
        fields = ['id', 'nombre']

class TteOpercionSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteOperacion
        fields = ['id', 'nombre']
