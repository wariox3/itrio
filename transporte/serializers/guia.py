from rest_framework import serializers
from transporte.models.guia import TteGuia


class TteGuiaSerializador(serializers.ModelSerializer):   
    operacion_ingreso__nombre = serializers.CharField(source='operacion_ingreso.nombre', read_only=True, allow_null=True, default=None)
    operacion_cargo__nombre = serializers.CharField(source='operacion_cargo.nombre', read_only=True, allow_null=True, default=None)
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True, allow_null=True, default=None)
    ciudad_origen__nombre = serializers.CharField(source='ciudad_origen.nombre', read_only=True, allow_null=True, default=None)
    ciudad_destino__nombre = serializers.CharField(source='ciudad_destino.nombre', read_only=True, allow_null=True, default=None)
    destinatario__nombre_corto = serializers.CharField(source='destinatario.nombre_corto', read_only=True, allow_null=True, default=None)
    destinatario__direccion = serializers.CharField(source='destinatario.direccion', read_only=True, allow_null=True, default=None)
    destinatario__telefono= serializers.CharField(source='destinatario.telefono', read_only=True, allow_null=True, default=None)
    destinatario__correo= serializers.CharField(source='destinatario.correo', read_only=True, allow_null=True, default=None)
    servicio__nombre= serializers.CharField(source='servicio.nombre', read_only=True, allow_null=True, default=None)
    producto__nombre= serializers.CharField(source='producto.nombre', read_only=True, allow_null=True, default=None)
    empaque__nombre= serializers.CharField(source='empaque.nombre', read_only=True, allow_null=True, default=None)
    ruta__nombre= serializers.CharField(source='ruta.nombre', read_only=True, allow_null=True, default=None)
    zona__nombre= serializers.CharField(source='zona.nombre', read_only=True, allow_null=True, default=None)
    class Meta:
        model = TteGuia
        fields = ['id', 'fecha', 'destinatario', 'destinatario__nombre_corto' , 'destinatario__direccion', 'destinatario__telefono', 'destinatario__correo' ,'ciudad_destino', 
                  'ciudad_destino__nombre' , 'ciudad_origen', 'ciudad_origen__nombre' ,'cliente', 'contacto', 'contacto__nombre_corto' , 'empaque', 'empaque__nombre',
                  'servicio', 'servicio__nombre','producto', 'producto__nombre', 'ruta', 'ruta__nombre', 'zona', 'zona__nombre' ,'operacion_cargo', 'operacion_cargo__nombre' ,'operacion_ingreso', 'operacion_ingreso__nombre', 'unidades', 'peso',
                  'volumen', 'peso_facturado', 'declara', 'flete', 'manejo', 'recaudo', 'cobro_entrega', 'contenido_verificado', 'remitente_nombre', 
                  'mercancia_peligrosa', 'requiere_cita', 'comentario', 'documento', 'fecha_ingreso', 'fecha_entrega' ,'despacho', 'estado_recogido', 'estado_ingreso', 'estado_embarcado',
                  'estado_despachado', 'estado_entregado', 'estado_soporte', 'estado_novedad', 'estado_novedad_solucionada', 'estado_rndc', 'numero_rndc', 'liquidacion']
        select_related_fields = ['contacto', 'destinatario', 'ciudad_destino', 'ciudad_origen', 'cliente', 'empaque', 
                                 'servicio', 'producto', 'ruta', 'zona', 'operacion_cargo', 'operacion_ingreso', 'despacho']  
    
 