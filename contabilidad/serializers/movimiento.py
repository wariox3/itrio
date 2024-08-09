from rest_framework import serializers
from contabilidad.models.movimiento import ConMovimiento
from contabilidad.models.cuenta import ConCuenta
from contabilidad.models.comprobante import ConComprobante
from general.models.contacto import GenContacto
from general.models.documento import GenDocumento

class ConMovimientoSerializador(serializers.HyperlinkedModelSerializer):    
    comprobante = serializers.PrimaryKeyRelatedField(queryset=ConComprobante.objects.all())
    cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all())
    contacto = serializers.PrimaryKeyRelatedField(queryset=GenContacto.objects.all(), allow_null=True)
    documento = serializers.PrimaryKeyRelatedField(queryset=GenDocumento.objects.all(), allow_null=True)

    class Meta:
        model = ConMovimiento
        fields = ['id', 'numero', 'fecha', 'debito', 'credito', 'base', 'naturaleza', 'cuenta', 'comprobante', 'contacto', 'documento']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'numero': instance.numero            
        }         
        