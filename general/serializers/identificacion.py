from general.models.identificacion import GenIdentificacion
from rest_framework import serializers

class GenIdentificacionSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenIdentificacion
        fields = ['id', 'nombre']  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'tipo_persona_id': instance.tipo_persona_id
        }        

class GenIdentificacionListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenIdentificacion

    def to_representation(self, instance):
        return {
            'identificacion_id': instance.id,            
            'identificacion_nombre': instance.nombre,
            'identificacion_tipo_persona_id': instance.tipo_persona_id
        }     