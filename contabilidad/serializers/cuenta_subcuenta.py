from rest_framework import serializers
from contabilidad.models.cuenta_subcuenta import ConCuentaSubcuenta

class ConCuentaSubcuentaSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConCuentaSubcuenta
        fields = ['id', 'nombre']

class ConCuentaSubcuentaListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConCuentaSubcuenta

    def to_representation(self, instance):
        return {
            'cuenta_subcuenta_id': instance.id,
            'cuenta_subcuenta_nombre': instance.nombre
        }        
        