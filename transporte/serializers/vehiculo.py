from rest_framework import serializers
from transporte.models.vehiculo import TteVehiculo

class TteVehiculoSerializador(serializers.ModelSerializer):    
    poseedor__nombre_corto = serializers.CharField(source='poseedor.nombre_corto', read_only=True)
    poseedor__numero_identificacion = serializers.CharField(source='poseedor.numero_identificacion', read_only=True)
    propietario__nombre_corto = serializers.CharField(source='propietario.nombre_corto', read_only=True)
    propietario__numero_identificacion = serializers.CharField(source='propietario.numero_identificacion', read_only=True)
    aseguradora__nombre_corto = serializers.CharField(source='aseguradora.nombre_corto', read_only=True)
    color__nombre = serializers.CharField(source='color.nombre', read_only=True)
    color__codigo = serializers.CharField(source='color.codigo', read_only=True)
    marca__nombre = serializers.CharField(source='marca.nombre', read_only=True)
    marca__codigo = serializers.CharField(source='marca.codigo', read_only=True)
    linea__nombre = serializers.CharField(source='linea.nombre', read_only=True)
    linea__codigo = serializers.CharField(source='linea.codigo', read_only=True)
    combustible__nombre = serializers.CharField(source='combustible.nombre', read_only=True)
    combustible__codigo = serializers.CharField(source='combustible.codigo', read_only=True)
    carroceria__nombre = serializers.CharField(source='carroceria.nombre', read_only=True)
    carroceria__codigo = serializers.CharField(source='carroceria.codigo', read_only=True)    
    configuracion__nombre = serializers.CharField(source='configuracion.nombre', read_only=True)
    configuracion__codigo = serializers.CharField(source='configuracion.codigo', read_only=True)    
    class Meta:
        model = TteVehiculo
        fields = ['id', 'fecha_registro', 'placa', 'modelo', 'modelo_repotenciado',
                  'motor', 'chasis', 'ejes', 'peso_vacio', 'capacidad', 'celular',
                  'poliza', 'vence_poliza', 'tecnicomecanica', 'vence_tecnicomecanica',
                  'propio', 'remolque', 'estado_inactivo', 'estado_revisado', 'comentario',
                  'poseedor', 'poseedor__nombre_corto', 'poseedor__numero_identificacion' ,'propietario', 'propietario__nombre_corto', 
                  'propietario__numero_identificacion', 'aseguradora', 'aseguradora__nombre_corto', 'color', 'color__nombre', 'color__codigo',
                  'marca', 'marca__nombre', 'marca__codigo', 'linea', 'linea__nombre', 'linea__codigo',
                  'combustible', 'combustible__nombre', 'combustible__codigo', 'carroceria', 'carroceria__nombre', 'carroceria__codigo',
                  'configuracion', 'configuracion__nombre', 'configuracion__codigo']
        select_related_fields = ['poseedor', 'propietario' , 'aseguradora', 'color', 'marca', 'linea', 'combustible', 'carroceria', 'configuracion']  
