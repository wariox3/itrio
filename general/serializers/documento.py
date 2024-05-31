from rest_framework import serializers
from general.models.documento import Documento
from general.models.documento_tipo import DocumentoTipo
from general.models.contacto import Contacto
from general.models.metodo_pago import MetodoPago
from general.models.empresa import Empresa
from general.models.plazo_pago import PlazoPago

class DocumentoSerializador(serializers.HyperlinkedModelSerializer):    
    numero = serializers.IntegerField(allow_null=True, label='Numero', default=None)
    fecha = serializers.DateField(allow_null=True, label='Fecha', default=None)
    fecha_vence = serializers.DateField(allow_null=True, label='Vence', default=None)
    fecha_contable = serializers.DateField(allow_null=True, label='Fecha contable', default=None)
    descuento = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, label='Descuento')
    base_impuesto = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, label='Base Impuesto')
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, label='Subtotal')    
    impuesto = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, label='Impuesto')
    total = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, label='Total')
    estado_aprobado = serializers.BooleanField(default = False, label='APR')    
    contacto = serializers.PrimaryKeyRelatedField(queryset=Contacto.objects.all(), allow_null=True)
    documento_tipo = serializers.PrimaryKeyRelatedField(queryset=DocumentoTipo.objects.all())    
    metodo_pago = serializers.PrimaryKeyRelatedField(queryset=MetodoPago.objects.all(), default=None, allow_null=True)
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all(), default=1)    
    documento_referencia = serializers.PrimaryKeyRelatedField(queryset=Documento.objects.all(), default=None, allow_null=True)    
    plazo_pago = serializers.PrimaryKeyRelatedField(queryset=PlazoPago.objects.all(), default=None, allow_null=True)    
    class Meta:
        model = Documento
        fields = ['id', 'numero', 'fecha', 'fecha_contable', 'fecha_vence', 'descuento', 'subtotal', 'impuesto', 'total', 'estado_aprobado', 'contacto', 'documento_tipo', 'metodo_pago', 'empresa', 'base_impuesto', 'estado_anulado', 'comentario', 'estado_electronico', 'soporte', 'estado_electronico_enviado', 'estado_electronico_notificado', 'orden_compra', 'documento_referencia', 'plazo_pago', 'cue']

    def to_representation(self, instance):        
        contacto = instance.contacto
        contacto_nombre_corto = None
        if contacto:
            contacto_nombre_corto = contacto.nombre_corto
        return {
            'id': instance.id,            
            'numero' : instance.numero,
            'fecha' : instance.fecha,
            'fecha_vence' : instance.fecha_vence,
            'fecha_contable' : instance.fecha_contable,
            'descuento': instance.descuento,
            'base_impuesto': instance.base_impuesto,           
            'subtotal': instance.subtotal,            
            'impuesto': instance.impuesto,
            'total' :  instance.total,
            'afectado' :  instance.afectado,
            'pendiente': instance.pendiente,
            'estado_aprobado' : instance.estado_aprobado,
            'contacto' : instance.contacto_id,            
            'documento_tipo': instance.documento_tipo_id,
            'metodo_pago': instance.metodo_pago_id,
            'contacto_id': instance.contacto_id,
            'contacto_nombre_corto': contacto_nombre_corto,
            'estado_anulado' : instance.estado_anulado,
            'comentario' : instance.comentario,
            'estado_electronico' : instance.estado_electronico,
            'estado_electronico_enviado' : instance.estado_electronico_enviado,
            'estado_electronico_notificado' : instance.estado_electronico_notificado,
            'soporte' : instance.soporte,
            'orden_compra' : instance.orden_compra,
            'cue' : instance.cue,
            'empresa': instance.empresa_id,
            'resolucion': instance.resolucion_id,
            'documento_referencia' :  instance.documento_referencia_id,
            'plazo_pago': instance.plazo_pago_id
        }
    
class DocumentoRetrieveSerializador(serializers.HyperlinkedModelSerializer):    
    contacto = serializers.PrimaryKeyRelatedField(queryset=Contacto.objects.all(), allow_null=True)
    documento_tipo = serializers.PrimaryKeyRelatedField(queryset=DocumentoTipo.objects.all())    
    documento_referencia = serializers.PrimaryKeyRelatedField(queryset=Documento.objects.all(), allow_null=True)    
    plazo_pago = serializers.PrimaryKeyRelatedField(queryset=PlazoPago.objects.all(), allow_null=True)    
    class Meta:
        model = Documento
        fields = ['id', 'numero', 'fecha', 'fecha_vence', 'descuento', 'subtotal', 'impuesto', 'total', 'estado_aprobado', 'contacto', 'documento_tipo', 'metodo_pago', 'base_impuesto', 'estado_anulado', 'comentario', 'estado_electronico', 'soporte', 'estado_electronico_enviado', 'estado_electronico_notificado', 'orden_compra', 'documento_referencia', 'plazo_pago', 'cue']

    def to_representation(self, instance):
        contacto = instance.contacto
        contacto_nombre_corto = ""
        if contacto is not None:
            contacto_nombre_corto = contacto.nombre_corto
        metodo_pago = instance.metodo_pago
        metodo_pago_nombre = ""
        if metodo_pago is not None:
            metodo_pago_nombre = metodo_pago.nombre            
        plazo_pago = instance.plazo_pago
        plazo_pago_nombre = ""
        if plazo_pago is not None:
            plazo_pago_nombre = plazo_pago.nombre       
        documento_referencia = instance.documento_referencia
        documento_referencia_numero = ""
        if documento_referencia is not None:
            documento_referencia_numero = documento_referencia.numero     
        return {
            'id': instance.id,            
            'numero' : instance.numero,
            'fecha' : instance.fecha,
            'fecha_vence' : instance.fecha_vence, 
            'contacto_id' : instance.contacto_id,
            'contacto_nombre_corto' : contacto_nombre_corto,
            'descuento': instance.descuento,
            'base_impuesto': instance.base_impuesto,
            'subtotal': instance.subtotal,  
            'pendiente': instance.pendiente,          
            'impuesto': instance.impuesto,
            'total' :  instance.total,        
            'estado_aprobado' : instance.estado_aprobado,
            'documento_tipo_id' : instance.documento_tipo_id,
            'metodo_pago_id' : instance.metodo_pago_id,
            'metodo_pago_nombre' : metodo_pago_nombre,
            'estado_anulado' :instance.estado_anulado,
            'comentario': instance.comentario,
            'estado_electronico' : instance.estado_electronico,
            'estado_electronico_enviado' : instance.estado_electronico_enviado,
            'estado_electronico_notificado' : instance.estado_electronico_notificado,
            'soporte' : instance.soporte,
            'orden_compra': instance.orden_compra,
            'plazo_pago_id': instance.plazo_pago_id,
            'plazo_pago_nombre': plazo_pago_nombre,
            'documento_referencia_id': instance.documento_referencia_id,
            'documento_referencia_numero': documento_referencia_numero,
            'cue' : instance.cue,
            'electronico_id': instance.electronico_id
        }

class DocumentoExcelSerializador(serializers.HyperlinkedModelSerializer):    
    numero = serializers.IntegerField(allow_null=True, label='Numero')
    fecha = serializers.DateField(allow_null=True, label='Fecha')
    fecha_vence = serializers.DateField(allow_null=True, label='Vence')
    descuento = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, label='Descuento')
    base_impuesto = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, label='Base Impuesto')
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, label='Subtotal')    
    impuesto = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, label='Impuesto')
    total = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, label='Total')
    estado_aprobado = serializers.BooleanField(default = False, label='APR')    
    contacto = serializers.PrimaryKeyRelatedField(queryset=Contacto.objects.all(), allow_null=True)
    documento_tipo = serializers.PrimaryKeyRelatedField(queryset=DocumentoTipo.objects.all())    
    metodo_pago = serializers.PrimaryKeyRelatedField(queryset=MetodoPago.objects.all(), allow_null=True)
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())    
    class Meta:
        model = Documento
        fields = ['id', 'numero', 'fecha', 'fecha_vence', 'descuento', 'subtotal', 'impuesto', 'total', 'estado_aprobado', 'contacto', 'documento_tipo', 'metodo_pago', 'empresa', 'base_impuesto', 'estado_anulado', 'comentario', 'estado_electronico', 'soporte', 'estado_electronico_enviado', 'estado_electronico_notificado', 'orden_compra']

    def to_representation(self, instance):        
        contacto = instance.contacto
        contacto_nombre_corto = None
        if contacto:
            contacto_nombre_corto = contacto.nombre_corto
        return {
            'id': instance.id,            
            'tipo': instance.documento_tipo_id,
            'numero' : instance.numero,
            'fecha' : instance.fecha,
            'fecha_vence' : instance.fecha_vence,            
            'metodo_pago': instance.metodo_pago_id,
            'orden_compra' : instance.orden_compra,
            'contacto_id': instance.contacto_id,
            'identificacion': instance.contacto.numero_identificacion if instance.contacto else None,
            'contacto': contacto_nombre_corto,
            'descuento': instance.descuento,            
            'subtotal': instance.subtotal,            
            'base_impuesto': instance.base_impuesto,           
            'impuesto': instance.impuesto,
            'total' :  instance.total,        
            'aprobado' : instance.estado_aprobado,
            'anulado' : instance.estado_anulado,
            'electronico' : instance.estado_electronico,
            'ele_enviado' : instance.estado_electronico_enviado,
            'ele_notificado' : instance.estado_electronico_notificado,        
            'empresa': instance.empresa_id,
            'resolucion': instance.resolucion_id,
            'comentario' : instance.comentario,
        }    
    
class DocumentoReferenciaSerializador(serializers.HyperlinkedModelSerializer):    
    numero = serializers.IntegerField(allow_null=True, label='Numero')
    class Meta:
        model = Documento
        fields = ['id', 'numero']

    def to_representation(self, instance):        
        return {
            'id': instance.id,            
            'numero' : instance.numero
        }   

class DocumentoInformeSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = Documento        

    def to_representation(self, instance):        
        contacto = instance.contacto
        contacto_nombre_corto = None
        if contacto:
            contacto_nombre_corto = contacto.nombre_corto
        return {
            'id': instance.id,            
            'numero' : instance.numero,
            'fecha' : instance.fecha,
            'fecha_vence' : instance.fecha_vence,
            'fecha_contable' : instance.fecha_contable,
            'descuento': instance.descuento,
            'base_impuesto': instance.base_impuesto,           
            'subtotal': instance.subtotal,            
            'impuesto': instance.impuesto,
            'total' :  instance.total, 
            'pendiente':instance.pendiente,       
            'estado_aprobado' : instance.estado_aprobado,
            'contacto' : instance.contacto_id,            
            'documento_tipo': instance.documento_tipo_id,
            'metodo_pago': instance.metodo_pago_id,
            'contacto_id': instance.contacto_id,
            'contacto_nombre_corto': contacto_nombre_corto,
            'estado_anulado' : instance.estado_anulado,
            'comentario' : instance.comentario,
            'estado_electronico' : instance.estado_electronico,
            'estado_electronico_enviado' : instance.estado_electronico_enviado,
            'estado_electronico_notificado' : instance.estado_electronico_notificado,
            'soporte' : instance.soporte,
            'orden_compra' : instance.orden_compra,
            'cue' : instance.cue,
            'empresa': instance.empresa_id,
            'resolucion': instance.resolucion_id,
            'documento_referencia' :  instance.documento_referencia_id,
            'plazo_pago': instance.plazo_pago_id
        }
    
class DocumentoAdicionarSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = Documento        

    def to_representation(self, instance):        
        contacto = instance.contacto
        contacto_nombre_corto = None
        if contacto:
            contacto_nombre_corto = contacto.nombre_corto
        documento_tipo_cuenta_cobrar_id = ""
        documento_tipo_cuenta_cobrar_cuenta_codigo = ""
        documento_tipo = instance.documento_tipo
        if documento_tipo:
            documento_tipo_cuenta_cobrar_id = documento_tipo.cuenta_cobrar_id
            cuenta_cobrar = documento_tipo.cuenta_cobrar
            if cuenta_cobrar:
                documento_tipo_cuenta_cobrar_cuenta_codigo = cuenta_cobrar.codigo
        return {
            'id': instance.id,            
            'numero' : instance.numero,
            'fecha' : instance.fecha,
            'fecha_vence' : instance.fecha_vence,
            'fecha_contable' : instance.fecha_contable,
            'descuento': instance.descuento,
            'base_impuesto': instance.base_impuesto,           
            'subtotal': instance.subtotal,            
            'impuesto': instance.impuesto,
            'total' :  instance.total, 
            'pendiente':instance.pendiente,       
            'estado_aprobado' : instance.estado_aprobado,
            'contacto' : instance.contacto_id,            
            'documento_tipo': instance.documento_tipo_id,
            'documento_tipo_cuenta_cobrar_id': documento_tipo_cuenta_cobrar_id,
            'documento_tipo_cuenta_cobrar_cuenta_codigo':documento_tipo_cuenta_cobrar_cuenta_codigo,
            'metodo_pago': instance.metodo_pago_id,
            'contacto_id': instance.contacto_id,
            'contacto_nombre_corto': contacto_nombre_corto,
            'estado_anulado' : instance.estado_anulado,
            'comentario' : instance.comentario,
            'estado_electronico' : instance.estado_electronico,
            'estado_electronico_enviado' : instance.estado_electronico_enviado,
            'estado_electronico_notificado' : instance.estado_electronico_notificado,
            'soporte' : instance.soporte,
            'orden_compra' : instance.orden_compra,
            'cue' : instance.cue,
            'empresa': instance.empresa_id,
            'resolucion': instance.resolucion_id,
            'documento_referencia' :  instance.documento_referencia_id,
            'plazo_pago': instance.plazo_pago_id
        }    
         