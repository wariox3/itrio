from rest_framework import serializers
from general.models.documento import Documento
from general.models.documento_tipo import DocumentoTipo
from general.models.resolucion import Resolucion
from general.models.contacto import Contacto
from general.models.metodo_pago import MetodoPago
from general.models.empresa import Empresa

class DocumentoSerializador(serializers.HyperlinkedModelSerializer):    
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
        fields = ['id', 'numero', 'fecha', 'fecha_vence', 'descuento', 'subtotal', 'impuesto', 'total', 'estado_aprobado', 'contacto', 'documento_tipo', 'metodo_pago', 'empresa', 'base_impuesto', 'estado_anulado', 'comentario', 'estado_electronico', 'soporte', 'estado_electronico_enviado', 'estado_electronico_notificado', 'resolucion']

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
            'descuento': instance.descuento,
            'base_impuesto': instance.base_impuesto,           
            'subtotal': instance.subtotal,            
            'impuesto': instance.impuesto,
            'total' :  instance.total,        
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
            'soporte' : instance.soporte
        }
    
class DocumentoRetrieveSerializador(serializers.HyperlinkedModelSerializer):    
    contacto = serializers.PrimaryKeyRelatedField(queryset=Contacto.objects.all(), allow_null=True)
    documento_tipo = serializers.PrimaryKeyRelatedField(queryset=DocumentoTipo.objects.all())    
    metodo_pago = serializers.PrimaryKeyRelatedField(queryset=MetodoPago.objects.all(), allow_null=True)
    class Meta:
        model = Documento
        fields = ['id', 'numero', 'fecha', 'fecha_vence', 'descuento', 'subtotal', 'impuesto', 'total', 'estado_aprobado', 'contacto', 'documento_tipo', 'metodo_pago', 'base_impuesto', 'estado_anulado', 'comentario', 'estado_electronico', 'soporte', 'estado_electronico_enviado', 'estado_electronico_notificado']

    def to_representation(self, instance):
        contacto = instance.contacto
        contacto_nombre_corto = ""
        if contacto is not None:
            contacto_nombre_corto = contacto.nombre_corto
        metodo_pago = instance.metodo_pago
        metodo_pago_nombre = ""
        if metodo_pago is not None:
            metodo_pago_nombre = metodo_pago.nombre            
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
            'soporte' : instance.soporte
        }