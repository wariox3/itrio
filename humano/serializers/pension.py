from rest_framework import serializers
from humano.models.pension import HumPension

class HumPensionSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumPension
        fields = ['id', 'nombre']

    

class HumPensionListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumPension

    def to_representation(self, instance):
        return {
            'pension_id': instance.id,
            'pension_nombre': instance.nombre,
        }         
        