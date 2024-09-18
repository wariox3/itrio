from rest_framework import serializers
from humano.models.periodo import HumPeriodo

class HumPeriodoSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumPeriodo
        fields = ['id', 'nombre', 'codigo', 'dias']

    

class HumPeriodoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HumPeriodo
    def to_representation(self, instance):
        return {
            'periodo_id': instance.id,
            'periodo_nombre': instance.nombre,
        }         
        