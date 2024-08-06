from contenedor.models import CtnCiudad
from rest_framework import serializers

class CtnCiudadSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CtnCiudad
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
     
class CtnCiudadListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = CtnCiudad

    def to_representation(self, instance):
        estado_nombre = ''        
        if instance.estado:
            estado_nombre = instance.estado.nombre
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'estado_nombre': estado_nombre
        }