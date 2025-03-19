from rest_framework import serializers
from ruteo.models.vehiculo import RutVehiculo

class RutVehiculoSerializador(serializers.HyperlinkedModelSerializer):        
    class Meta:
        model = RutVehiculo
        fields = ['id', 'placa', 'capacidad', 'tiempo', 'estado_activo', 'estado_asignado', 'franja_id', 'franja_codigo', 'usuario_app']

    def to_representation(self, instance):        
        return {
            'id': instance.id, 
            'placa': instance.placa,
            'capacidad': instance.capacidad,
            'tiempo': instance.tiempo,
            'estado_activo': instance.estado_activo,
            'estado_asignado': instance.estado_asignado,
            'franja_id': instance.franja_id,            
            'franja_codigo': instance.franja_codigo, 
            'usuario_app': instance.usuario_app           
        }
    
