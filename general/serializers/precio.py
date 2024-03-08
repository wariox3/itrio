from general.models.precio import Precio
from rest_framework import serializers

class PrecioSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Precio
        fields = ['id', 'nombre', 'tipo', 'fecha_vence']

    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'tipo': instance.tipo,
            'fecha_vence': instance.fecha_vence,
        }    