from general.models.ciudad import GenCiudad
from rest_framework import serializers

class GenCiudadSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenCiudad
        fields = [
            'id', 
            'nombre'
            ]  
        
    def to_representation(self, instance):
        nombre_ciudad = instance.nombre
        nombre_estado = instance.estado.nombre

        nombre_completo = f"{nombre_ciudad} - {nombre_estado}"

        return {
            'id': instance.id,            
            'nombre': nombre_completo,
        }
     
class GenCiudadListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenCiudad

    def to_representation(self, instance):
        nombre_ciudad = instance.nombre
        nombre_estado = instance.estado.nombre

        nombre_completo = f"{nombre_ciudad} - {nombre_estado}"

        return {
            'ciudad_id': instance.id,            
            'ciudad_nombre': nombre_completo,
        } 