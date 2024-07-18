from rest_framework import serializers
from ruteo.models.rut_vehiculo import RutVehiculo


class RutVehiculoSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = RutVehiculo
        fields = ['id', 'placa', 'capacidad', 'estado_activo', 'estado_asignado']

    def to_representation(self, instance):        
        return {
            'id': instance.id, 
            'placa': instance.placa,
            'capacidad': instance.capacidad,
            'estado_activo': instance.estado_activo,
            'estado_asignado': instance.estado_asignado
        }
    
