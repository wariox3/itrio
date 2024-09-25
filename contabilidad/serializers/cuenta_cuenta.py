from rest_framework import serializers
from contabilidad.models.cuenta_cuenta import ConCuentaCuenta

class ConCuentaCuentaSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConCuentaCuenta
        fields = ['id', 'nombre']

class ConCuentaCuentaListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConCuentaCuenta

    def to_representation(self, instance):
        return {
            'cuenta_cuenta_id': instance.id,
            'cuenta_cuenta_nombre': instance.nombre
        }        
        