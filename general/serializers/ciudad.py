from general.models.ciudad import Ciudad
from rest_framework import serializers

class CiudadSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ciudad
        fields = [
            'id', 
            'nombre'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }  
     
class CiudadListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Ciudad

    def to_representation(self, instance):
        return {
            'ciudad_id': instance.id,            
            'ciudad_nombre': instance.nombre,
        }           