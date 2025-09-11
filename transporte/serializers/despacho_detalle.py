from rest_framework import serializers
from transporte.models.despacho_detalle import TteDespachoDetalle

class TteDespachoDetalleSerializador(serializers.ModelSerializer):   
    guia__fecha = serializers.CharField(source='guia.fecha', read_only=True, allow_null=True, default=None)
    guia__ciudad_destino__nombre = serializers.CharField(source='guia.ciudad_destino.nombre', read_only=True, allow_null=True, default=None)
    guia__cliente__nombre_corto = serializers.CharField(source='guia.cliente.nombre_corto', read_only=True, allow_null=True, default=None)
    guia__estado_entregado = serializers.BooleanField(source='guia.estado_entregado', read_only=True, allow_null=True, default=None)    
    class Meta:
        model = TteDespachoDetalle
        fields = ['id', 'unidades', 'peso', 'volumen', 'cobro_entrega', 'despacho', 'guia',
                  'guia_id', 
                  'guia__fecha',
                  'guia__ciudad_destino__nombre', 
                  'guia__cliente__nombre_corto',
                  'guia__estado_entregado'] 
        select_related_fields = ['guia', 'guia__ciudad_destino', 'guia__cliente']     

class TteDespachoDetalleGuiaSerializador(serializers.ModelSerializer):   
    despacho__servicio__nombre = serializers.CharField(source='despacho.servicio.nombre', read_only=True, allow_null=True, default=None)
    despacho__fecha = serializers.CharField(source='despacho.fecha', read_only=True, allow_null=True, default=None)
    despacho__vehiculo__placa = serializers.CharField(source='despacho.vehiculo.placa', read_only=True, allow_null=True, default=None)
    despacho__conductor__nombre_corto = serializers.CharField(source='despacho.conductor.nombre_corto', read_only=True, allow_null=True, default=None)
    despacho__ciudad_origen__nombre = serializers.CharField(source='despacho.ciudad_origen.nombre', read_only=True, allow_null=True, default=None)
    despacho__ciudad_destino__nombre = serializers.CharField(source='despacho.ciudad_destino.nombre', read_only=True, allow_null=True, default=None)
    despacho__estado_aprobado = serializers.CharField(source='despacho.estado_aprobado', read_only=True, allow_null=True, default=None)
    class Meta:
        model = TteDespachoDetalle
        fields = ['id', 
                  'despacho_id',
                  'despacho__fecha',
                  'despacho__servicio__nombre',
                  'despacho__vehiculo__placa',
                  'despacho__conductor__nombre_corto',
                  'despacho__ciudad_origen__nombre',
                  'despacho__ciudad_destino__nombre',  
                  'despacho__estado_aprobado'                                 
                ] 
        select_related_fields = ['despacho', 'despacho__servicio', 'despacho__vehiculo', 'despacho__conductor', 'despacho__ciudad_origen', 'despacho__ciudad_destino']           
 