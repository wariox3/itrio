from rest_framework import serializers
from general.models.documento import Documento
from general.models.documento_tipo import DocumentoTipo
from general.models.contacto import Contacto

class ContactoSerializador(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = ['nombre_corto', 'numero_identificacion']

class DocumentoTipoSerializador(serializers.ModelSerializer):
    documento_tipo_id = serializers.IntegerField(source='id')
    
    class Meta:
        model = DocumentoTipo
        fields = ['documento_tipo_id', 'nombre']

class DocumentoSerializador(serializers.HyperlinkedModelSerializer):    
    documentoTipo = DocumentoTipoSerializador(source='documento_tipo')
    contacto_id = serializers.PrimaryKeyRelatedField(source='contacto', queryset=Contacto.objects.all(), write_only=True)
    
    class Meta:
        model = Documento
        fields = ['id', 'subtotal', 'descuento', 'impuesto', 'total_bruto', 'total', 'fecha', 'documentoTipo', 'contacto_id', 'numero', 'fecha_vence']
