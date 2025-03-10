from rest_framework import serializers
from ruteo.models.vehiculo import RutVehiculo
from ruteo.models.franja import RutFranja

class RutVehiculoSerializador(serializers.HyperlinkedModelSerializer):    
    franja = serializers.PrimaryKeyRelatedField(queryset=RutFranja.objects.all(), default=None, allow_null=True)
    class Meta:
        model = RutVehiculo
        fields = ['id', 'placa', 'capacidad', 'tiempo', 'estado_activo', 'estado_asignado', 'franja']

    def to_representation(self, instance):        
        franja_nombre = ''
        franja_codigo = ''
        if instance.franja:
            franja_nombre = instance.franja.nombre
            franja_codigo = instance.franja.codigo 
        return {
            'id': instance.id, 
            'placa': instance.placa,
            'capacidad': instance.capacidad,
            'tiempo': instance.tiempo,
            'estado_activo': instance.estado_activo,
            'estado_asignado': instance.estado_asignado,
            'franja_id': instance.franja_id,
            'franja_codigo': franja_codigo,
            'franja_nombre': franja_nombre,
        }
    
