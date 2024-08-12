from rest_framework import serializers
from humano.models.grupo import HumGrupo

class HumGrupoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumGrupo
        fields = ['id', 'nombre']

class HumGrupoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumGrupo

    def to_representation(self, instance):
        return {
            'grupo_id': instance.id,
            'grupo_nombre': instance.nombre,
        }         
    
class HumGrupoListaBuscarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HumGrupo
        fields = ['id', 'nombre']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre
        }     