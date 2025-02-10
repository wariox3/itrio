from general.models.cuenta_banco import GenCuentaBanco
from general.models.cuenta_banco_tipo import GenCuentaBancoTipo
from general.models.cuenta_banco_clase import GenCuentaBancoClase
from contabilidad.models.cuenta import ConCuenta
from rest_framework import serializers

class GenCuentaBancoSerializador(serializers.HyperlinkedModelSerializer):
    cuenta_banco_tipo = serializers.PrimaryKeyRelatedField(queryset=GenCuentaBancoTipo.objects.all())
    cuenta_banco_clase = serializers.PrimaryKeyRelatedField(queryset=GenCuentaBancoClase.objects.all(), default=None, allow_null=True)
    cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    class Meta:
        model = GenCuentaBanco
        fields = ['id', 'cuenta_banco_tipo', 'cuenta_banco_clase', 'nombre', 'numero_cuenta', 'cuenta']

    def to_representation(self, instance):
        cuenta_banco_tipo_nombre = ""
        if instance.cuenta_banco_tipo:
            cuenta_banco_tipo_nombre = instance.cuenta_banco_tipo.nombre
        cuenta_banco_clase_nombre = ""
        if instance.cuenta_banco_clase:
            cuenta_banco_clase_nombre = instance.cuenta_banco_clase.nombre
        cuenta_nombre = ''
        cuenta_codigo = ''
        if instance.cuenta:
            cuenta_nombre = instance.cuenta.nombre
            cuenta_codigo = instance.cuenta.codigo            
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'numero_cuenta': instance.numero_cuenta,
            'cuenta_banco_tipo_id': instance.cuenta_banco_tipo_id,
            'cuenta_banco_tipo_nombre': cuenta_banco_tipo_nombre,
            'cuenta_banco_clase_id': instance.cuenta_banco_clase_id,
            'cuenta_banco_clase_nombre': cuenta_banco_clase_nombre,
            'cuenta_id': instance.cuenta_id,
            'cuenta_codigo': cuenta_codigo,
            'cuenta_nombre': cuenta_nombre
        }
        
class GenCuentaBancoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenCuentaBancoTipo

    def to_representation(self, instance):
        return {
            'cuenta_banco_id': instance.id,            
            'cuenta_banco_nombre': instance.nombre,
        }      