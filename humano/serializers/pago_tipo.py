from rest_framework import serializers
from humano.models.pago_tipo import HumPagoTipo
from contabilidad.models.cuenta import ConCuenta

class HumPagoTipoSerializador(serializers.HyperlinkedModelSerializer):
    cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    
    class Meta:
        model = HumPagoTipo
        fields = ['id', 'nombre', 'cuenta']

class HumPagoTipoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumPagoTipo

    def to_representation(self, instance):
        return {
            'pago_tipo_id': instance.id,
            'pago_tipo_nombre': instance.nombre,
        }          