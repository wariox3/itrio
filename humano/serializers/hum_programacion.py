from rest_framework import serializers
from humano.models.hum_programacion import HumProgramacion

class HumProgramacionSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumProgramacion
        fields = ['id']
        