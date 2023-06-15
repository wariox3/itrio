from general.models.tipo_persona import TipoPersona
from rest_framework import serializers

class TipoPersonaSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TipoPersona
        fields = [
            'id', 
            'nombre'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }        