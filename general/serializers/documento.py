from rest_framework import serializers
from general.models.documento import Documento
from general.models.documento_tipo import DocumentoTipo

class DocumentoSerializador(serializers.HyperlinkedModelSerializer):    
    documento_tipo = serializers.PrimaryKeyRelatedField(queryset=DocumentoTipo.objects.all())    
    class Meta:
        model = Documento
        fields = ['id', 'documento_tipo', 'subtotal', 'descuento', 'impuesto', 'total_bruto', 'total', 'fecha', 'contacto', 'numero', 'fecha_vence']

    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'documento_tipo_id': instance.documento_tipo_id,
            'subtotal': instance.subtotal,
            'descuento': instance.descuento,
            'impuesto': instance.impuesto,
            'total_bruto': instance.total_bruto,
            'total' :  instance.total,
            'fecha' : instance.fecha,
            'fecha_vence' : instance.fecha_vence,
            'contacto_id' : instance.contacto,
            'numero' : instance.numero
        }