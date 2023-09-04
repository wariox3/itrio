from general.models.identificacion import Identificacion
from rest_framework import serializers

class IdentificacionSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Identificacion
        fields = [
            'id', 
            'nombre'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }        

class IdentificacionListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Identificacion

    def to_representation(self, instance):
        return {
            'identificacion_id': instance.id,            
            'identificacion_nombre': instance.nombre,
        }     