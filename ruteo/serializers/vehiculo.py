from rest_framework import serializers
from ruteo.models.vehiculo import RutVehiculo

class RutVehiculoSerializador(serializers.ModelSerializer):
    franjas_codigo = serializers.SerializerMethodField()
    class Meta:
        model = RutVehiculo
        fields = [
            'id', 'placa', 'capacidad', 'tiempo', 
            'estado_activo', 'estado_asignado', 'usuario_app',
            'prioridad', 'franjas_codigo'
        ]

    def get_franjas_codigo(self, obj):
        return list(obj.franjas.values_list('codigo', flat=True))
