from rest_framework import serializers
from transporte.models.guia import TteGuia


class TteGuiaSerializador(serializers.ModelSerializer):   
    operacion_ingreso__nombre = serializers.CharField(source='operacion_ingreso.nombre', read_only=True)
    operacion_cargo__nombre = serializers.CharField(source='operacion_cargo.nombre', read_only=True)
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True)
    ciudad_origen__nombre = serializers.CharField(source='ciudad_origen.nombre', read_only=True)
    ciudad_destino__nombre = serializers.CharField(source='ciudad_destino.nombre', read_only=True)
    class Meta:
        model = TteGuia
        fields = ['id', 'fecha', 'destinatario', 'ciudad_destino', 'ciudad_destino__nombre' , 'ciudad_origen', 'ciudad_origen__nombre' ,'cliente', 'contacto', 'contacto__nombre_corto' , 'empaque',
                  'servicio', 'producto', 'ruta', 'zona', 'operacion_cargo', 'operacion_cargo__nombre' ,'operacion_ingreso', 'operacion_ingreso__nombre', 'unidades', 'peso',
                  'volumen', 'peso_facturado', 'declara', 'flete', 'manejo', 'recaudo', 'cobro_entrega', 'contenido_verificado',
                  'mercancia_peligrosa', 'requiere_cita', 'comentario', 'documento', 'fecha_ingreso', 'despacho', 'estado_recogido', 'estado_ingreso', 'estado_embarcado',
                  'estado_despachado', 'estado_entregado', 'estado_soporte', 'estado_novedad', 'estado_novedad_solucionada', 'estado_rndc']
        select_related_fields = ['contacto', 'destinatario', 'ciudad_destino', 'ciudad_origen', 'cliente', 'empaque'
                                 'servicio', 'producto', 'ruta', 'zona', 'operacion_cargo', 'operacion_ingreso', 'despacho']  
    
 