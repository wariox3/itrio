from rest_framework import serializers
from transporte.models.conductor import TteConductor

class TteConductorSerializador(serializers.ModelSerializer):    
    identificacion__nombre = serializers.CharField(source='identificacion.nombre', read_only=True)
    ciudad__nombre = serializers.CharField(source='ciudad.nombre', read_only=True)
    ciudad__estado__nombre = serializers.CharField(source='ciudad.estado.nombre', read_only=True)
    rh__nombre = serializers.CharField(source='rh.nombre', read_only=True)
    rh__codigo = serializers.CharField(source='rh.codigo', read_only=True) 
    class Meta:
        model = TteConductor
        fields = ['id', 'identificacion', 'identificacion__nombre', 'ciudad' ,'ciudad__nombre' ,'ciudad__estado__nombre', 'rh', 'rh__nombre', 'rh__codigo',
                  'numero_identificacion', 'nombre_corto', 'nombre1', 'nombre2', 'apellido1', 'apellido2',
                  'direccion', 'barrio', 'telefono', 'celular', 'correo', 'numero_licencia', 'categoria_licencia', 'fecha_nacimiento',
                  'fecha_vence_licencia', 'fecha_expedicion_licencia', 'fecha_ingreso', 'fecha_retiro',
                  'propio', 'estado_inactivo', 'estado_revisado', 'comentario']
        select_related_fields = ['identificacion', 'ciudad', 'ciudad__estado', 'rh']  
