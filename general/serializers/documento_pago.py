from general.models.documento_pago import DocumentoPago
from general.models.documento import Documento
from general.models.cuenta_banco import CuentaBanco
from rest_framework import serializers

class DocumentoPagoSerializador(serializers.HyperlinkedModelSerializer):
    documento = serializers.PrimaryKeyRelatedField(queryset=Documento.objects.all())
    cuenta_banco = serializers.PrimaryKeyRelatedField(queryset=CuentaBanco.objects.all())
    class Meta:
        model = DocumentoPago
        fields = ['documento', 'cuenta_banco', 'pago']

    def to_representation(self, instance):
        return {
            'id': instance.id, 
            'documento_id': instance.documento_id,           
            'pago': instance.pago,
        }  
