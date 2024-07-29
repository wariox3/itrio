from rest_framework import serializers
from contabilidad.models.con_cuenta import ConCuenta

class CuentaSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConCuenta
        fields = ['id', 'cuenta_clase_id']

class CuentaListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConCuenta

    def to_representation(self, instance):

        return {
            'cuenta_id': instance.id,
            'cuenta_codigo': instance.codigo,            
            'cuenta_nombre': instance.nombre
        }         
        