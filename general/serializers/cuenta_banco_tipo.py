from general.models.cuenta_banco_tipo import CuentaBancoTipo
from rest_framework import serializers

class GenCuentaBancoTipoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = CuentaBancoTipo
        fields = ['id', 'nombre']

    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }  

class GenCuentaBancoTipoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = CuentaBancoTipo

    def to_representation(self, instance):
        return {
            'cuenta_banco_tipo_id': instance.id,            
            'cuenta_banco_tipo_nombre': instance.nombre,
        }       