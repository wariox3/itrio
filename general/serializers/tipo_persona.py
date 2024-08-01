from general.models.tipo_persona import GenTipoPersona
from rest_framework import serializers

class GenTipoPersonaSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenTipoPersona
        fields = [
            'id', 
            'nombre'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }   
         
class GenTipoPersonaListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenTipoPersona

    def to_representation(self, instance):
        return {
            'tipo_persona_id': instance.id,            
            'tipo_persona_nombre': instance.nombre,
        }       