from rest_framework import serializers
from inventario.models.almacen import InvAlmacen

class InvAlmacenSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = InvAlmacen
        fields = ['id', 'nombre']

class InvAlmacenListaSerializador(serializers.ModelSerializer):          
    class Meta:
        model = InvAlmacen
        fields = ['id', 
                  'nombre']


class InvAlmacenListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = InvAlmacen

    def to_representation(self, instance):
        return {
            'almacen_id': instance.id,
            'almacen_nombre': instance.nombre,
        }         
        