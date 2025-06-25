from general.models.tipo_persona import GenTipoPersona
from rest_framework import serializers

class GenTipoPersonaSerializador(serializers.ModelSerializer):
    class Meta:
        model = GenTipoPersona
        fields = ['id', 'nombre']  
         