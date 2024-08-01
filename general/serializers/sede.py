from general.models.sede import Sede
from rest_framework import serializers

class GenSedeSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sede
        fields = [
            'id',
            'nombre', 
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre    
        }     

class GenSedeListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sede
        
    def to_representation(self, instance):
        return {
            'sede_id': instance.id,            
            'sede_nombre': instance.nombre
        }       