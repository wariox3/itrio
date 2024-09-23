from rest_framework import serializers
from contabilidad.models.cuenta_grupo import ConCuentaGrupo

class ConCuentaGrupoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConCuentaGrupo
        fields = ['id', 'nombre']

class ConCuentaGrupoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConCuentaGrupo

    def to_representation(self, instance):
        return {
            'cuenta_grupo_id': instance.id,
            'cuenta_grupo_nombre': instance.nombre
        }        
        