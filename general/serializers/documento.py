from rest_framework import serializers
from general.models.documento import Documento
from general.models.documento_tipo import DocumentoTipo
from general.models.contacto import Contacto

class ContactoSerializador(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = ['nombre_corto', 'numero_identificacion']

class DocumentoTipoSerializador(serializers.ModelSerializer):
    class Meta:
        model = DocumentoTipo
        fields = ['documento_tipo_id', 'nombre']

class DocumentoSerializador(serializers.HyperlinkedModelSerializer):    
    documentoTipo = DocumentoTipoSerializador()
    contacto = ContactoSerializador()    
    class Meta:
        model = Documento
        fields = ['id', 'subtotal', 'descuento', 'impuesto', 'total_bruto', 'total', 'fecha', 'contacto', 'numero', 'fecha_vence']

    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'subtotal': instance.subtotal,
            'descuento': instance.descuento,
            'impuesto': instance.impuesto,
            'total_bruto': instance.total_bruto,
            'total' :  instance.total,
            'fecha' : instance.fecha,
            'fecha_vence' : instance.fecha_vence,
            'contacto_id' : instance.contacto_id,
            'numero' : instance.numero
        }