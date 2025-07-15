from rest_framework import serializers
from transporte.models.vehiculo_configuracion import TteVehiculoConfiguracion

class TteConfiguracionSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteVehiculoConfiguracion
        fields = ['id', 'nombre']

class TteConfiguracionSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteVehiculoConfiguracion
        fields = ['id', 'nombre']
