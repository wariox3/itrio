from general.models.parametros import GenParametros

from rest_framework import serializers
from decouple import config

class GenParametrosSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenParametros
        fields = ['uvt', 'factor', 'salario_minimo', 'auxilio_transporte']          