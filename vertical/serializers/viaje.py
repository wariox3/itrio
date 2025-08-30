from rest_framework import serializers
from vertical.models.viaje import VerViaje

class VerViajeSerializador(serializers.ModelSerializer):
    class Meta:
        model = VerViaje
        fields = ['id', 'fecha', 'cliente', 'unidades', 'peso', 'volumen', 'negocio_id', 'contenedor_id', 'schema_name', 'solicitud_cliente', 
                  'estado_aceptado', 'flete', 'puntos_entrega', 'comentario',
                  'vehiculo', 
                  'conductor',
                  'usuario', 
                  'ciudad_origen', 
                  'ciudad_destino']        

class VerViajeListaSerializador(serializers.ModelSerializer):
    ciudad_origen__nombre = serializers.CharField(source='ciudad_origen.nombre', read_only=True, allow_null=True, default=None)
    ciudad_destino__nombre = serializers.CharField(source='ciudad_destino.nombre', read_only=True, allow_null=True, default=None)
    class Meta:
        model = VerViaje
        fields = ['id', 'fecha', 'cliente', 'unidades', 'peso', 'volumen', 'puntos_entrega', 'comentario', 
                  'ciudad_origen_id',
                  'ciudad_origen__nombre',
                  'ciudad_destino_id',
                  'ciudad_destino__nombre']
        select_related_fields = ['ciudad_origen', 'ciudad_destino']          
        