from rest_framework import serializers
from humano.models.sucursal import HumSucursal

class HumSucursalSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumSucursal
        fields = ['id', 'nombre']

    

class HumSucursalListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumSucursal

    def to_representation(self, instance):
        return {
            'sucursal_id': instance.id,
            'sucursal_nombre': instance.nombre,
        }         
        