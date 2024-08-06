from general.models.ciudad import GenCiudad
from rest_framework import serializers

class GenCiudadSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenCiudad
        fields = ['id', 'nombre']  
        
    def to_representation(self, instance):
        estado_nombre = ''        
        if instance.estado:
            estado_nombre = instance.estado.nombre
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'estado_nombre': estado_nombre
        }
     
class GenCiudadListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenCiudad

    def to_representation(self, instance):
        estado_nombre = ''        
        if instance.estado:
            estado_nombre = instance.estado.nombre
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'estado_nombre': estado_nombre
        }