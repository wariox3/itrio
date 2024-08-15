from rest_framework import serializers
from humano.models.salud import HumSalud

class HumSaludSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumSalud
        fields = ['id', 'nombre']

    

class HumSaludListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumSalud

    def to_representation(self, instance):
        return {
            'salud_id': instance.id,
            'salud_nombre': instance.nombre,
        }         
        