from rest_framework import serializers
from transporte.models.negocio import TteNegocio

class TteNegocioSerializador(serializers.ModelSerializer):   
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True, allow_null=True, default=None)
    ciudad_origen__nombre = serializers.CharField(source='ciudad_origen.nombre', read_only=True, allow_null=True, default=None)
    ciudad_destino__nombre = serializers.CharField(source='ciudad_destino.nombre', read_only=True, allow_null=True, default=None)
    class Meta:
        model = TteNegocio
        fields = ['id', 'fecha', 'fecha_registro', 'unidades' , 'peso', 'volumen', 'declara' ,'pago', 
                  'flete' , 'manejo', 'comentario', 
                  'contacto',  
                  'contacto__nombre_corto', 
                  'ciudad_origen',
                  'ciudad_origen__nombre' ,
                  'ciudad_destino', 
                  'ciudad_destino__nombre']
        select_related_fields = ['contacto', 'ciudad_origen', 'ciudad_destino']  