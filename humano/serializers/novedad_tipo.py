from rest_framework import serializers
from humano.models.novedad_tipo import HumNovedadTipo

class HumNovedadTipoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumNovedadTipo
        fields = ['id', 'nombre', 'novedad_clase_id']

    def to_representation(self, instance):      

        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'novedad_clase_id': instance.novedad_clase_id
        }       

class HumNovedadTipoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumNovedadTipo

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'novedad_clase_id': instance.novedad_clase_id
        }        