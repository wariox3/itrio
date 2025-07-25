from rest_framework import serializers
from humano.models.contrato_tipo import HumContratoTipo

class HumContratoTipoSeleccionarSerializador(serializers.ModelSerializer):
    class Meta:
        model = HumContratoTipo
        fields = ['id', 'nombre']

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