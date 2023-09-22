from contenedor.models import ContenedorIdentificacion
from rest_framework import serializers

class ContenedorIdentificacionSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContenedorIdentificacion
        fields = [
            'id', 
            'nombre'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }        

class ContenedorIdentificacionListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ContenedorIdentificacion

    def to_representation(self, instance):
        return {
            'identificacion_id': instance.id,            
            'identificacion_nombre': instance.nombre,
        }     