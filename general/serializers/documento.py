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
        fields = ['id', 'nombre']

class DocumentoSerializador(serializers.HyperlinkedModelSerializer):    
    documentoTipo = DocumentoTipoSerializador()
    contacto = ContactoSerializador()    
    class Meta:
        model = Documento
        fields = ['id', 'subtotal', 'descuento', 'impuesto', 'total_bruto', 'total', 'fecha', 'contacto', 'numero', 'fecha_vence']
