from rest_framework import serializers
from general.models.documento import Documento
from general.models.documento_tipo import DocumentoTipo

class DocumentoSerializador(serializers.HyperlinkedModelSerializer):    
    documento_tipo = serializers.PrimaryKeyRelatedField(queryset=DocumentoTipo.objects.all())    
    class Meta:
        model = Documento
        fields = ['id', 'documento_tipo', 'subtotal', 'descuento', 'impuesto', 'total_bruto', 'total']
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'documento_tipo': instance.documento_tipo,
            'subtotal': instance.subtotal,
            'descuento': instance.descuento,
            'impuesto': instance.impuesto,
            'total_bruto': instance.total_bruto,
            'total' :  instance.total
        }