from rest_framework import serializers
from transporte.models.guia import TteGuia


class TteGuiaSerializador(serializers.ModelSerializer):   
    operacion_ingreso__nombre = serializers.CharField(source='operacion_ingreso.nombre', read_only=True, allow_null=True, default=None)
    operacion_cargo__nombre = serializers.CharField(source='operacion_cargo.nombre', read_only=True, allow_null=True, default=None)
    cliente__nombre_corto = serializers.CharField(source='cliente.nombre_corto', read_only=True, allow_null=True, default=None)
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True, allow_null=True, default=None)
    ciudad_origen__nombre = serializers.CharField(source='ciudad_origen.nombre', read_only=True, allow_null=True, default=None)
    ciudad_destino__nombre = serializers.CharField(source='ciudad_destino.nombre', read_only=True, allow_null=True, default=None)
    servicio__nombre= serializers.CharField(source='servicio.nombre', read_only=True, allow_null=True, default=None)
    producto__nombre= serializers.CharField(source='producto.nombre', read_only=True, allow_null=True, default=None)
    empaque__nombre= serializers.CharField(source='empaque.nombre', read_only=True, allow_null=True, default=None)
    ruta__nombre= serializers.CharField(source='ruta.nombre', read_only=True, allow_null=True, default=None)
    zona__nombre= serializers.CharField(source='zona.nombre', read_only=True, allow_null=True, default=None)
    negocio__nombre= serializers.CharField(source='negocio.nombre', read_only=True, allow_null=True, default=None)
    class Meta:
        model = TteGuia
        fields = ['id', 'fecha', 'destinatario_nombre', 'destinatario_direccion', 'destinatario_telefono', 'destinatario_correo',
                  'unidades', 'peso',
                  'volumen', 'peso_facturado', 'declara', 'flete', 'manejo', 'recaudo', 'cobro_entrega', 'contenido_verificado', 'remitente_nombre', 
                  'mercancia_peligrosa', 'requiere_cita', 'comentario', 'documento', 'fecha_ingreso', 'fecha_entrega', 'fecha_recogida', 'fecha_despacho', 'fecha_soporte', 'estado_recogido', 'estado_ingreso', 'estado_embarcado',
                  'estado_despachado', 'estado_entregado', 'estado_soporte', 'estado_novedad', 'estado_novedad_solucionada', 'estado_rndc', 'numero_rndc', 'liquidacion',                  
                  'cliente', 
                  'cliente__nombre_corto',
                  'contacto', 
                  'contacto__nombre_corto', 
                  'negocio',
                  'negocio__nombre',
                  'ciudad_origen', 
                  'ciudad_origen__nombre',
                  'ciudad_destino', 
                  'ciudad_destino__nombre', 
                  'destinatario',
                  'empaque', 
                  'empaque__nombre',
                  'servicio', 
                  'servicio__nombre',
                  'producto', 
                  'producto__nombre', 
                  'ruta', 
                  'ruta__nombre', 
                  'zona', 
                  'zona__nombre',
                  'operacion_cargo', 
                  'operacion_cargo__nombre',
                  'operacion_ingreso', 
                  'operacion_ingreso__nombre', 
                  'despacho'
                ]
        select_related_fields = ['contacto', 'destinatario', 'ciudad_destino', 'ciudad_origen', 'cliente', 'empaque', 
                                 'servicio', 'producto', 'ruta', 'zona', 'operacion_cargo', 'operacion_ingreso', 'despacho', 'negocio']  
    
class TteGuiaDetalleSerializador(serializers.ModelSerializer):   
    operacion_ingreso__nombre = serializers.CharField(source='operacion_ingreso.nombre', read_only=True, allow_null=True, default=None)
    operacion_cargo__nombre = serializers.CharField(source='operacion_cargo.nombre', read_only=True, allow_null=True, default=None)
    cliente__nombre_corto = serializers.CharField(source='cliente.nombre_corto', read_only=True, allow_null=True, default=None)
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True, allow_null=True, default=None)
    ciudad_origen__nombre = serializers.CharField(source='ciudad_origen.nombre', read_only=True, allow_null=True, default=None)
    ciudad_destino__nombre = serializers.CharField(source='ciudad_destino.nombre', read_only=True, allow_null=True, default=None)
    servicio__nombre= serializers.CharField(source='servicio.nombre', read_only=True, allow_null=True, default=None)
    producto__nombre= serializers.CharField(source='producto.nombre', read_only=True, allow_null=True, default=None)
    empaque__nombre= serializers.CharField(source='empaque.nombre', read_only=True, allow_null=True, default=None)
    ruta__nombre= serializers.CharField(source='ruta.nombre', read_only=True, allow_null=True, default=None)
    zona__nombre= serializers.CharField(source='zona.nombre', read_only=True, allow_null=True, default=None)
    class Meta:
        model = TteGuia
        fields = ['id', 'fecha', 'destinatario_nombre' , 'destinatario_direccion', 'destinatario_telefono', 'destinatario_correo',
                  'unidades', 'peso', 'volumen', 'peso_facturado', 'declara', 'flete', 'manejo', 'recaudo', 'cobro_entrega', 'contenido_verificado',
                  'mercancia_peligrosa', 'requiere_cita', 'comentario', 'documento', 'fecha_ingreso', 'fecha_entrega', 'fecha_recogida', 'fecha_despacho', 
                  'fecha_soporte' ,'despacho', 'estado_recogido', 'estado_ingreso', 'estado_embarcado', 'estado_despachado', 'estado_entregado', 
                  'estado_soporte', 'estado_novedad', 'estado_novedad_solucionada', 'estado_rndc', 'numero_rndc', 'liquidacion',
                  'cliente', 
                  'cliente__nombre_corto',
                  'contacto', 
                  'contacto__nombre_corto',
                  'ciudad_destino', 
                  'ciudad_destino__nombre', 
                  'ciudad_origen', 
                  'ciudad_origen__nombre', 
                  'empaque', 
                  'empaque__nombre',
                  'servicio', 
                  'servicio__nombre',
                  'producto', 
                  'producto__nombre', 
                  'ruta', 
                  'ruta__nombre', 
                  'zona', 
                  'zona__nombre',
                  'operacion_cargo', 
                  'operacion_cargo__nombre',
                  'operacion_ingreso', 
                  'operacion_ingreso__nombre',                   
                  'remitente_nombre'                   
                  ]
        select_related_fields = ['contacto', 'ciudad_destino', 'ciudad_origen', 'cliente', 'empaque', 
                                 'servicio', 'producto', 'ruta', 'zona', 'operacion_cargo', 'operacion_ingreso', 'despacho']  