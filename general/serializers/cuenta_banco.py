from general.models.cuenta_banco import CuentaBanco
from rest_framework import serializers

class CuentaBancoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = CuentaBanco
        fields = ['id', 'nombre']

    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }    