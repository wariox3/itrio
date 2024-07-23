from rest_framework import serializers
from humano.models.hum_grupo import HumGrupo

class HumGrupoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumGrupo
        fields = ['id', 'nombre']
        