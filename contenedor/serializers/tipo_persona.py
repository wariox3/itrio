from contenedor.models import ContenedorTipoPersona
from rest_framework import serializers

class ContenedorTipoPersonaSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContenedorTipoPersona
        fields = [
            'id', 
            'nombre'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }        

class ContenedorTipoPersonaListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ContenedorTipoPersona

    def to_representation(self, instance):
        return {
            'tipo_persona_id': instance.id,            
            'tipo_persona_nombre': instance.nombre,
        }     