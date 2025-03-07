from rest_framework import serializers
from humano.models.pago_tipo import HumPagoTipo

class HumPagoTipoSerializador(serializers.HyperlinkedModelSerializer):        
    class Meta:
        model = HumPagoTipo
        fields = ['id', 'nombre']

class HumPagoTipoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumPagoTipo

    def to_representation(self, instance):
        return {
            'pago_tipo_id': instance.id,
            'pago_tipo_nombre': instance.nombre,
        }          