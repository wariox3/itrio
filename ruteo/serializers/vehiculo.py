from rest_framework import serializers
from ruteo.models.vehiculo import RutVehiculo

class RutVehiculoSerializador(serializers.HyperlinkedModelSerializer):
    franja_id = serializers.SerializerMethodField()
    franja_codigo = serializers.SerializerMethodField()
    
    class Meta:
        model = RutVehiculo
        fields = [
            'id', 'placa', 'capacidad', 'tiempo', 
            'estado_activo', 'estado_asignado', 'usuario_app',
            'franja_id', 'franja_codigo', 'prioridad'
        ]

    def get_franja_id(self, obj):
        return list(obj.franjas.values_list('id', flat=True))

    def get_franja_codigo(self, obj):
        return list(obj.franjas.values_list('codigo', flat=True))

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['franja_id'] = self.get_franja_id(instance)
        representation['franja_codigo'] = self.get_franja_codigo(instance)
        return representation