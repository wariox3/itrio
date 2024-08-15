from rest_framework import serializers
from humano.models.cargo import HumCargo

class HumCargoSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumCargo
        fields = ['id', 'nombre']

    

class HumCargoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumCargo

    def to_representation(self, instance):
        return {
            'cargo_id': instance.id,
            'cargo_nombre': instance.nombre,
        }         
        