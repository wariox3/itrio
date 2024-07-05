from general.models.cuenta_banco import CuentaBanco
from general.models.cuenta_banco_tipo import CuentaBancoTipo
from rest_framework import serializers

class CuentaBancoSerializador(serializers.HyperlinkedModelSerializer):
    cuenta_banco_tipo = serializers.PrimaryKeyRelatedField(queryset=CuentaBancoTipo.objects.all())
    class Meta:
        model = CuentaBanco
        fields = ['id', 'cuenta_banco_tipo', 'nombre']

    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }    