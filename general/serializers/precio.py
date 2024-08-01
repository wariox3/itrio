from general.models.precio import GenPrecio
from rest_framework import serializers

class GenPrecioSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenPrecio
        fields = ['id', 'nombre', 'tipo', 'fecha_vence']

    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'tipo': instance.tipo,
            'fecha_vence': instance.fecha_vence,
        }    
    
class GenPrecioListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenPrecio 
        
    def to_representation(self, instance):
        return {
            'precio_id': instance.id,            
            'precio_nombre': instance.nombre
        }      