from general.models.cuenta_banco import CuentaBanco
from general.models.cuenta_banco_tipo import CuentaBancoTipo
from rest_framework import serializers

class GenCuentaBancoSerializador(serializers.HyperlinkedModelSerializer):
    cuenta_banco_tipo = serializers.PrimaryKeyRelatedField(queryset=CuentaBancoTipo.objects.all())
    class Meta:
        model = CuentaBanco
        fields = ['id', 'cuenta_banco_tipo', 'nombre', 'numero_cuenta']

    def to_representation(self, instance):
        cuenta_banco_tipo_nombre = ""
        if instance.cuenta_banco_tipo:
            cuenta_banco_tipo_nombre = instance.cuenta_banco_tipo.nombre
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'numero_cuenta': instance.numero_cuenta,
            'cuenta_banco_tipo_id': instance.cuenta_banco_tipo_id,
            'cuenta_banco_tipo_nombre': cuenta_banco_tipo_nombre
        }
        
class GenCuentaBancoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = CuentaBancoTipo

    def to_representation(self, instance):
        return {
            'cuenta_banco_id': instance.id,            
            'cuenta_banco_nombre': instance.nombre,
        }      