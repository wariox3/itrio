from rest_framework import serializers
from general.models.documento import Documento
from general.models.documento_tipo import DocumentoTipo
from general.models.contacto import Contacto

class ContactoSerializador(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = ['nombre_corto', 'numero_identificacion']

class DocumentoSerializador(serializers.HyperlinkedModelSerializer):    
    documento_tipo = serializers.PrimaryKeyRelatedField(queryset=DocumentoTipo.objects.all())    
    contacto = ContactoSerializador()
    nombre_corto = serializers.SerializerMethodField()  # Campo personalizado
    numero_identificacion = serializers.SerializerMethodField()  # Campo personalizado
    
    class Meta:
        model = Documento
        fields = ['id', 'documento_tipo', 'subtotal', 'descuento', 'impuesto', 'total_bruto', 'total', 'fecha', 'contacto', 'numero', 'fecha_vence', 'nombre_corto', 'numero_identificacion']

    def get_nombre_corto(self, instance):
        return instance.contacto.nombre_corto if instance.contacto else None
    
    def get_numero_identificacion(self, instance):
        return instance.contacto.numero_identificacion if instance.contacto else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)  # Obtener la representación predeterminada del objeto
        
        # Eliminar los campos de contacto del nivel superior
        representation.pop('contacto')
        
        return representation
