from rest_framework import serializers
from vertical.models.servicio import VerServicio

class VerServicioSerializador(serializers.ModelSerializer):
    class Meta:
        model = VerServicio
        fields = ['id', 'nombre']

class VerServicioSeleccionarSerializador(serializers.ModelSerializer):
    class Meta:
        model = VerServicio
        fields = ['id', 'nombre']        
        