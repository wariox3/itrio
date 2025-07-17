from rest_framework import serializers
from transporte.models.servicio import TteServicio

class TteServicioSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteServicio
        fields = ['id', 'nombre']

class TteSeervicioSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteServicio
        fields = ['id', 'nombre']
