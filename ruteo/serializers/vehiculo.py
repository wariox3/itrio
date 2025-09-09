from rest_framework import serializers
from ruteo.models.vehiculo import RutVehiculo

class RutVehiculoSerializador(serializers.HyperlinkedModelSerializer):   
    class Meta:
        model = RutVehiculo
        fields = [
            'id', 'placa', 'capacidad', 'tiempo', 
            'estado_activo', 'estado_asignado', 'usuario_app',
            'prioridad'
        ]