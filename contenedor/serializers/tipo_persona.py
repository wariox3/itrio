from contenedor.models import CtnTipoPersona
from rest_framework import serializers

class CtnTipoPersonaSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CtnTipoPersona
        fields = [
            'id', 
            'nombre'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }        

class CtnTipoPersonaListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = CtnTipoPersona

    def to_representation(self, instance):
        return {
            'tipo_persona_id': instance.id,            
            'tipo_persona_nombre': instance.nombre,
        }     