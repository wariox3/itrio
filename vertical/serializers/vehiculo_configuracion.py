from rest_framework import serializers
from vertical.models.vehiculo_configuracion import VerVehiculoConfiguracion

class VerVehiculoConfiguracionSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerVehiculoConfiguracion
        fields = ['id', 'nombre']
        