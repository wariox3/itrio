from general.models.documento_pago import GenDocumentoPago
from general.models.documento import GenDocumento
from general.models.cuenta_banco import GenCuentaBanco
from rest_framework import serializers

class GenDocumentoPagoSerializador(serializers.HyperlinkedModelSerializer):
    documento = serializers.PrimaryKeyRelatedField(queryset=GenDocumento.objects.all())
    cuenta_banco = serializers.PrimaryKeyRelatedField(queryset=GenCuentaBanco.objects.all())
    class Meta:
        model = GenDocumentoPago
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
