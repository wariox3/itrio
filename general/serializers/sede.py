from general.models.sede import GenSede
from rest_framework import serializers
from contabilidad.models.grupo import ConGrupo

class GenSedeSerializador(serializers.HyperlinkedModelSerializer):
    grupo__nombre = serializers.CharField(source='estado.nombre', read_only=True)
    class Meta:
        model = GenSede
        fields = ['id', 'nombre', 'grupo__nombre']  
        select_related_fields = ['grupo']        

  