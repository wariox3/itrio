from inquilino.models import InquilinoIdentificacion
from rest_framework import serializers

class InquilinoIdentificacionSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InquilinoIdentificacion
        fields = [
            'id', 
            'nombre'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }        

class InquilinoIdentificacionListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = InquilinoIdentificacion

    def to_representation(self, instance):
        return {
            'identificacion_id': instance.id,            
            'identificacion_nombre': instance.nombre,
        }     