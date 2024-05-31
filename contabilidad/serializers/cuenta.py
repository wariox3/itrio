from rest_framework import serializers
from contabilidad.models.cuenta import Cuenta

class CuentaSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Cuenta
        fields = ['id', 'cuenta_clase_id']

class CuentaListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Cuenta

    def to_representation(self, instance):

        return {
            'cuenta_id': instance.id,
            'cuenta_codigo': instance.codigo,            
            'cuenta_nombre': instance.nombre
        }         
        