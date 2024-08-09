from rest_framework import serializers
from contabilidad.models.grupo import ConGrupo

class ConGrupoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConGrupo
        fields = ['id', 'nombre', 'codigo']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'codigo': instance.codigo
        } 


class ConGrupoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConGrupo

    def to_representation(self, instance):
        return {
            'grupo_id': instance.id,
            'grupo_nombre': instance.nombre,
            'grupo_codigo': instance.codigo,
        }         
        