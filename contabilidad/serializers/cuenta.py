from rest_framework import serializers
from contabilidad.models.cuenta import ConCuenta

class ConCuentaSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConCuenta
        fields = ['id', 'cuenta_clase_id']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'codigo': instance.codigo
        } 


class ConCuentaListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConCuenta

    def to_representation(self, instance):
        return {
            'cuenta_id': instance.id,
            'cuenta_nombre': instance.nombre,
            'cuenta_codigo': instance.codigo
        }         
        