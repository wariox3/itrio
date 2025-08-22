from rest_framework import serializers
from transporte.models.despacho import TteDespacho

class TteDespachoSerializador(serializers.ModelSerializer):    
    despacho_tipo__nombre = serializers.CharField(source='despacho_tipo.nombre', read_only=True, allow_null=True, default=None)
    operacion__nombre = serializers.CharField(source='operacion.nombre', read_only=True, allow_null=True, default=None)
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True, allow_null=True, default=None)
    ciudad_origen__nombre = serializers.CharField(source='ciudad_origen.nombre', read_only=True, allow_null=True, default=None)
    ciudad_destino__nombre = serializers.CharField(source='ciudad_destino.nombre', read_only=True, allow_null=True, default=None)
    vehiculo__placa = serializers.CharField(source='vehiculo.placa', read_only=True, allow_null=True, default=None)
    remolque__placa = serializers.CharField(source='remolque.placa', read_only=True, allow_null=True, default=None)
    conductor__nombre_corto = serializers.CharField(source='conductor.nombre_corto', read_only=True, allow_null=True, default=None)
    ruta__nombre = serializers.CharField(source='ruta.nombre', read_only=True, allow_null=True, default=None)
    servicio__nombre = serializers.CharField(source='servicio.nombre', read_only=True, allow_null=True, default=None)
    class Meta:
        model = TteDespacho
        fields = ['id', 'fecha', 'numero', 'numero_rndc', 'fecha_salida', 'fecha_llegada', 'fecha_entrega', 'fecha_soporte', 'pago', 
                  'precinto', 'guias', 'unidades', 'peso', 'volumen', 'declara', 'flete',
                  'manejo', 'recaudo', 'cobro_entrega', 'comentario', 'estado_rndc', 
                  'estado_entregado', 'estado_soporte', 'despacho_tipo' ,'despacho_tipo__nombre', 'operacion' ,'operacion__nombre', 'contacto', 'contacto__nombre_corto', 
                  'ciudad_origen', 'ciudad_origen__nombre', 'ciudad_destino', 'ciudad_destino__nombre', 'vehiculo', 'vehiculo__placa', 'remolque', 'remolque__placa', 'conductor',
                  'conductor__nombre_corto', 'ruta', 'ruta__nombre', 'servicio', 'servicio__nombre']
        select_related_fields = ['despacho_tipo', 'operacion', 'contacto', 'ciudad_origen', 'ciudad_destino', 'vehiculo', 'remolque', 'conductor', 'ruta', 'servicio']  

