from rest_framework import serializers
from humano.models.sucursal import HumSucursal

class HumSucursalSeleccionarSerializador(serializers.ModelSerializer):
    class Meta:
        model = HumSucursal
        fields = ['id', 'nombre']

class HumSucursalSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumSucursal
        fields = ['id', 'codigo', 'nombre']

    

class HumSucursalListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumSucursal

    def to_representation(self, instance):
        return {
            'sucursal_id': instance.id,
            'sucursal_codigo': instance.codigo,
            'sucursal_nombre': instance.nombre,
        }         
        