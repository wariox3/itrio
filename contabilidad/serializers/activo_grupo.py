from rest_framework import serializers
from contabilidad.models.activo_grupo import ConActivoGrupo

class ConActivoGrupoSeleccionarSerializador(serializers.ModelSerializer):
    class Meta:
        model = ConActivoGrupo
        fields = ['id', 'nombre']

class ConActivoGrupoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConActivoGrupo
        fields = '__all__'

class ConActivoGrupoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConActivoGrupo

    def to_representation(self, instance):
        return {
            'activo_grupo_id': instance.id,
            'activo_grupo_nombre': instance.nombre
        }        
        