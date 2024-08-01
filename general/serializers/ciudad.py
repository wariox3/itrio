from general.models.ciudad import Ciudad
from rest_framework import serializers

class GenCiudadSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ciudad
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
        model = Ciudad

    def to_representation(self, instance):
        nombre_ciudad = instance.nombre
        nombre_estado = instance.estado.nombre

        nombre_completo = f"{nombre_ciudad} - {nombre_estado}"

        return {
            'ciudad_id': instance.id,            
            'ciudad_nombre': nombre_completo,
        } 