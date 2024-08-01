from general.models.cuenta_banco_tipo import GenCuentaBancoTipo
from rest_framework import serializers

class GenCuentaBancoTipoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenCuentaBancoTipo
        fields = ['id', 'nombre']

    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }  

class GenCuentaBancoTipoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenCuentaBancoTipo

    def to_representation(self, instance):
        return {
            'cuenta_banco_tipo_id': instance.id,            
            'cuenta_banco_tipo_nombre': instance.nombre,
        }       