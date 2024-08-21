from general.models.complemento import GenComplemento
from rest_framework import serializers

class GenComplementoSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenComplemento
        fields = ['id', 'nombre', 'instalado', 'datos_json']      