from rest_framework import serializers
from humano.models.hum_contrato_tipo import HumContratoTipo

class HumContratoTipoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumContratoTipo
        fields = ['id', 'nombre']

class HumContratoTipoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumContratoTipo

    def to_representation(self, instance):
        return {
            'contrato_tipo_id': instance.id,
            'contrato_tipo_nombre': instance.nombre,
        }         