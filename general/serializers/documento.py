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
        representation = super().to_representation(instance)  # Obtener la representación predeterminada del objeto

        # Obtener la representación de los objetos relacionados
        documento_tipo_representation = representation.pop('documentoTipo')
        contacto_representation = representation.pop('contacto')
        
        # Agregar los campos del serializador DocumentoTipoSerializador
        for field, value in documento_tipo_representation.items():
            representation[field] = value

        # Agregar los campos del serializador ContactoSerializador
        for field, value in contacto_representation.items():
            representation[field] = value
        
        return representation
