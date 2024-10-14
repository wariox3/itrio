from general.models.cuenta_banco_clase import GenCuentaBancoClase
from rest_framework import serializers

class GenCuentaBancoClaseSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenCuentaBancoClase
        fields = ['id', 'nombre']

    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }  

class GenCuentaBancoClaseListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenCuentaBancoClase

    def to_representation(self, instance):
        return {
            'cuenta_banco_clase_id': instance.id,            
            'cuenta_banco_clase_nombre': instance.nombre,
        }       