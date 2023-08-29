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
        fields = ['nombre']

class DocumentoSerializador(serializers.HyperlinkedModelSerializer):    
    documentoTipo = DocumentoTipoSerializador()
    contacto = ContactoSerializador()    
    class Meta:
        model = Documento
        fields = ['id', 'documento_tipo', 'subtotal', 'descuento', 'impuesto', 'total_bruto', 'total', 'fecha', 'contacto', 'numero', 'fecha_vence', 'contacto_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)  # Obtener la representación predeterminada del objeto

        # Agregar los campos personalizados
        representation['nombre_corto'] = instance.contacto.nombre_corto if instance.contacto else None
        representation['numero_identificacion'] = instance.contacto.numero_identificacion if instance.contacto else None
        representation['nombre'] = instance.documento_tipo.nombre if instance.documento_tipo else None
        
        return representation
