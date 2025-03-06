from rest_framework import serializers
from humano.models.tipo_costo import HumTipoCosto

class HumTipoCostoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumTipoCosto
        fields = ['id', 'nombre']

class HumTipoCostoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumTipoCosto

    def to_representation(self, instance):
        return {
            'tipo_costo_id': instance.id,
            'tipo_costo_nombre': instance.nombre,
        }          