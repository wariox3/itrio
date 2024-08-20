from rest_framework import serializers
from humano.models.concepto_tipo import HumConceptoTipo

class HumConceptoTipoSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumConceptoTipo
        fields = ['id', 'nombre']

    

class HumConceptoTipoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumConceptoTipo

    def to_representation(self, instance):
        return {
            'concepto_tipo_id': instance.id,
            'concepto_tipo_nombre': instance.nombre,
        }         
        