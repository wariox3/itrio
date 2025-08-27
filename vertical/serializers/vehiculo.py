from rest_framework import serializers
from vertical.models.vehiculo import VerVehiculo

class VerVehiculoSerializador(serializers.ModelSerializer):
    color__nombre = serializers.CharField(source='color.nombre', read_only=True, allow_null=True, default=None)
    color__codigo = serializers.CharField(source='color.codigo', read_only=True, allow_null=True, default=None)
    marca__nombre = serializers.CharField(source='marca.nombre', read_only=True, allow_null=True, default=None)
    marca__codigo = serializers.CharField(source='marca.codigo', read_only=True, allow_null=True, default=None)
    linea__nombre = serializers.CharField(source='linea.nombre', read_only=True, allow_null=True, default=None)
    linea__codigo = serializers.CharField(source='linea.codigo', read_only=True, allow_null=True, default=None)
    combustible__nombre = serializers.CharField(source='combustible.nombre', read_only=True, allow_null=True, default=None)
    combustible__codigo = serializers.CharField(source='combustible.codigo', read_only=True, allow_null=True, default=None)
    carroceria__nombre = serializers.CharField(source='carroceria.nombre', read_only=True, allow_null=True, default=None)
    carroceria__codigo = serializers.CharField(source='carroceria.codigo', read_only=True, allow_null=True, default=None)    
    configuracion__nombre = serializers.CharField(source='configuracion.nombre', read_only=True, allow_null=True, default=None)
    configuracion__codigo = serializers.CharField(source='configuracion.codigo', read_only=True, allow_null=True, default=None)    
    class Meta:
        model = VerVehiculo
        fields = ['id', 'placa', 'modelo', 'modelo_repotenciado', 'motor', 'chasis', 'ejes', 'peso_vacio', 'capacidad',
                'poliza', 'vence_poliza', 'tecnicomecanica', 'vence_tecnicomecanica', 'propio', 'remolque', 'color', 'color__nombre', 'color__codigo',
                'marca', 'marca__nombre', 'marca__codigo', 'linea', 'linea__nombre', 'linea__codigo',
                'combustible', 'combustible__nombre', 'combustible__codigo', 'carroceria', 'carroceria__nombre', 'carroceria__codigo',
                'configuracion', 'configuracion__nombre', 'configuracion__codigo']
        select_related_fields = ['color', 'marca', 'linea', 'combustible', 'carroceria', 'configuracion']  
        