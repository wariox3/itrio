from rest_framework import serializers
from general.models.documento import Documento
from general.models.documento_tipo import DocumentoTipo
from general.models.contacto import Contacto

class DocumentoSerializador(serializers.HyperlinkedModelSerializer):    
    numero = serializers.IntegerField(allow_null=True, label='Numero')
    fecha = serializers.DateField(allow_null=True, label='Fecha')
    fecha_vence = serializers.DateField(allow_null=True, label='Vence')
    descuento = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, label='Descuento')
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, label='Subtotal')    
    impuesto = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, label='Impuesto')
    total = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, label='Total')
    estado_aprobado = serializers.BooleanField(default = False, label='APR')    
    contacto = serializers.PrimaryKeyRelatedField(queryset=Contacto.objects.all(), allow_null=True)
    documento_tipo = serializers.PrimaryKeyRelatedField(queryset=DocumentoTipo.objects.all())    
    class Meta:
        model = Documento
        fields = ['id', 'numero', 'fecha', 'fecha_vence', 'descuento', 'subtotal', 'impuesto', 'total', 'estado_aprobado', 'contacto', 'documento_tipo']

    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'numero' : instance.numero,
            'fecha' : instance.fecha,
            'fecha_vence' : instance.fecha_vence,            
            'descuento': instance.descuento,
            'subtotal': instance.subtotal,            
            'impuesto': instance.impuesto,
            'total' :  instance.total,        
            'estado_aprobado' : instance.estado_aprobado,
            'contacto' : instance.contacto_id,            
            'documento_tipo': instance.documento_tipo_id
        }
    
class DocumentoRetrieveSerializador(serializers.HyperlinkedModelSerializer):    
    contacto = serializers.PrimaryKeyRelatedField(queryset=Contacto.objects.all(), allow_null=True)
    documento_tipo = serializers.PrimaryKeyRelatedField(queryset=DocumentoTipo.objects.all())    
    class Meta:
        model = Documento
        fields = ['id', 'numero', 'fecha', 'fecha_vence', 'descuento', 'subtotal', 'impuesto', 'total', 'estado_aprobado', 'contacto', 'documento_tipo']

    def to_representation(self, instance):
        contacto = instance.contacto
        contacto_nombre_corto = ""
        if contacto is not None:
            contacto_nombre_corto = contacto.nombre_corto
        return {
            'id': instance.id,            
            'numero' : instance.numero,
            'fecha' : instance.fecha,
            'fecha_vence' : instance.fecha_vence, 
            'contacto_id' : instance.contacto,
            'contacto_nombre_corto' : contacto_nombre_corto,
            'descuento': instance.descuento,
            'subtotal': instance.subtotal,            
            'impuesto': instance.impuesto,
            'total' :  instance.total,        
            'estado_aprobado' : instance.estado_aprobado,
            'documento_tipo_id' : instance.documento_tipo_id
        }