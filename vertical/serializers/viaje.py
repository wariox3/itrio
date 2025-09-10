from rest_framework import serializers
from vertical.models.viaje import VerViaje
from vertical.serializers.propuesta import VerPropuestaSerializador

class VerViajeSerializador(serializers.ModelSerializer):
    ciudad_origen__nombre = serializers.CharField(source='ciudad_origen.nombre', read_only=True, allow_null=True, default=None)
    ciudad_destino__nombre = serializers.CharField(source='ciudad_destino.nombre', read_only=True, allow_null=True, default=None)
    servicio__nombre = serializers.CharField(source='servicio.nombre', read_only=True, allow_null=True, default=None)
    producto__nombre = serializers.CharField(source='producto.nombre', read_only=True, allow_null=True, default=None)
    empaque__nombre = serializers.CharField(source='empaque.nombre', read_only=True, allow_null=True, default=None)
    usuario__nombre_corto = serializers.CharField(source='usuario.nombre_corto', read_only=True, allow_null=True, default=None)     
    class Meta:
        model = VerViaje
        fields = [  
                    'id', 'fecha', 'cliente', 'unidades', 'peso', 'volumen', 'negocio_id', 'contenedor_id', 'schema_name', 
                    'solicitud_cliente', 'solicitud_transporte',
                    'estado_aceptado', 'estado_cancelado', 'flete', 'pago', 'puntos_entrega', 'comentario', 'propuestas',
                    'vehiculo', 
                    'conductor',
                    'ciudad_origen',
                    'ciudad_origen_id',
                    'ciudad_origen__nombre',
                    'ciudad_destino',
                    'ciudad_destino_id',
                    'ciudad_destino__nombre',
                    'servicio',
                    'servicio_id',
                    'servicio__nombre',
                    'producto',
                    'producto_id',
                    'producto__nombre',
                    'empaque',
                    'empaque_id',
                    'empaque__nombre',
                    'usuario',
                    'usuario_id',
                    'usuario__nombre_corto',                     
                ]        
        select_related_fields = ['ciudad_origen', 'ciudad_destino', 'servicio', 'producto', 'empaque', 'usuario']

class VerViajeListaSerializador(serializers.ModelSerializer):
    ciudad_origen__nombre = serializers.CharField(source='ciudad_origen.nombre', read_only=True, allow_null=True, default=None)
    ciudad_destino__nombre = serializers.CharField(source='ciudad_destino.nombre', read_only=True, allow_null=True, default=None)
    servicio__nombre = serializers.CharField(source='servicio.nombre', read_only=True, allow_null=True, default=None)
    producto__nombre = serializers.CharField(source='producto.nombre', read_only=True, allow_null=True, default=None)
    empaque__nombre = serializers.CharField(source='empaque.nombre', read_only=True, allow_null=True, default=None)    
    class Meta:
        model = VerViaje
        fields = [  'id', 'fecha', 'cliente', 'unidades', 'peso', 'volumen', 'puntos_entrega', 'comentario', 'propuestas',
                    'ciudad_origen_id',
                    'ciudad_origen__nombre',
                    'ciudad_destino_id',
                    'ciudad_destino__nombre',
                    'servicio_id',
                    'servicio__nombre',
                    'producto_id',
                    'producto__nombre',
                    'empaque_id',
                    'empaque__nombre'               
                  ]
        select_related_fields = ['ciudad_origen', 'ciudad_destino', 'servicio', 'producto', 'empaque'] 

class VerViajeListaEspecialSerializador(serializers.ModelSerializer):
    ciudad_origen__nombre = serializers.CharField(source='ciudad_origen.nombre', read_only=True, allow_null=True, default=None)
    ciudad_destino__nombre = serializers.CharField(source='ciudad_destino.nombre', read_only=True, allow_null=True, default=None)
    servicio__nombre = serializers.CharField(source='servicio.nombre', read_only=True, allow_null=True, default=None)
    producto__nombre = serializers.CharField(source='producto.nombre', read_only=True, allow_null=True, default=None)
    empaque__nombre = serializers.CharField(source='empaque.nombre', read_only=True, allow_null=True, default=None)
    usuario__nombre_corto = serializers.CharField(source='usuario.nombre_corto', read_only=True, allow_null=True, default=None)    
    class Meta:
        model = VerViaje
        fields = [  'id', 'fecha', 'cliente', 'unidades', 'peso', 'volumen', 'puntos_entrega', 'comentario', 'propuestas', 'estado_aceptado',
                    'ciudad_origen_id',
                    'ciudad_origen__nombre',
                    'ciudad_destino_id',
                    'ciudad_destino__nombre',
                    'servicio_id',
                    'servicio__nombre',
                    'producto_id',
                    'producto__nombre',
                    'empaque_id',
                    'empaque__nombre',
                    'usuario_id',
                    'usuario__nombre_corto',               
                  ]                 
        