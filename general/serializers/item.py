from general.models.item import Item
from rest_framework import serializers

class ItemSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Item
        fields = ['id', 'codigo', 'nombre', 'referencia', 'costo', 'precio']

    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'codigo': instance.codigo,
            'nombre': instance.nombre,
            'referencia': instance.referencia,
            'costo': instance.costo,
            'precio': instance.precio
        } 