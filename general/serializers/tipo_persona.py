from general.models.tipo_persona import TipoPersona
from rest_framework import serializers

class GenTipoPersonaSerializador(serializers.HyperlinkedModelSerializer):
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
         
class GenTipoPersonaListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = TipoPersona

    def to_representation(self, instance):
        return {
            'tipo_persona_id': instance.id,            
            'tipo_persona_nombre': instance.nombre,
        }       