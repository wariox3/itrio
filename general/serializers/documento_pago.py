from general.models.documento_pago import DocumentoPago
from general.models.documento import Documento
from general.models.cuenta_banco import CuentaBanco
from rest_framework import serializers

class GenDocumentoPagoSerializador(serializers.HyperlinkedModelSerializer):
    documento = serializers.PrimaryKeyRelatedField(queryset=Documento.objects.all())
    cuenta_banco = serializers.PrimaryKeyRelatedField(queryset=CuentaBanco.objects.all())
    class Meta:
        model = DocumentoPago
        fields = ['documento', 'cuenta_banco', 'pago']

    def to_representation(self, instance):
        cuenta_banco_nombre = ""
        if instance.cuenta_banco:
            cuenta_banco_nombre = instance.cuenta_banco.nombre
        return {
            'id': instance.id, 
            'documento_id': instance.documento_id,           
            'pago': instance.pago,
            'cuenta_banco_id': instance.cuenta_banco_id,
            'cuenta_banco_nombre': cuenta_banco_nombre
        }  
