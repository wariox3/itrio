from rest_framework import serializers
from humano.models.grupo import HumGrupo
from humano.models.periodo import HumPeriodo

class HumGrupoSerializador(serializers.HyperlinkedModelSerializer):
    periodo = serializers.PrimaryKeyRelatedField(queryset=HumPeriodo.objects.all(), default=None, allow_null=True)
    class Meta:
        model = HumGrupo
        fields = ['id', 'nombre', 'periodo']
        
    def to_representation(self, instance):
        periodo_dias = 0
        if instance.periodo:
            periodo_dias = instance.periodo.dias
        return {
            'grupo_id': instance.id,
            'grupo_nombre': instance.nombre,
            'grupo_periodo_id': instance.periodo_id,
            'grupo_periodo_dias': periodo_dias
        }         

class HumGrupoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = HumGrupo
    
    def to_representation(self, instance):
        periodo_dias = 0
        if instance.periodo:
            periodo_dias = instance.periodo.dias
        return {
            'grupo_id': instance.id,
            'grupo_nombre': instance.nombre,
            'grupo_periodo_id': instance.periodo_id,
            'grupo_periodo_dias': periodo_dias
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