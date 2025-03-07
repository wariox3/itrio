from rest_framework import serializers
from humano.models.configuracion_provision import HumConfiguracionProvision
from humano.models.tipo_costo import HumTipoCosto
from contabilidad.models.cuenta import ConCuenta

class HumConfiguracionProvisionSerializador(serializers.HyperlinkedModelSerializer):
    tipo_costo = serializers.PrimaryKeyRelatedField(queryset=HumTipoCosto.objects.all(), default=None, allow_null=True)
    cuenta_debito = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    cuenta_credito = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)

    class Meta:
        model = HumConfiguracionProvision
        fields = ['id', 'cuenta_credito', 'cuenta_debito', 'tipo_costo']    

    def to_representation(self, instance):       
        tipo_costo_nombre = ""
        if instance.tipo_costo:
            tipo_costo_nombre = instance.tipo_costo.nombre
        cuenta_debito_nombre = ""
        cuenta_debito_codigo = ""
        if instance.cuenta_debito:
            cuenta_debito_nombre = instance.cuenta_debito.nombre
            cuenta_debito_codigo = instance.cuenta_debito.codigo
        cuenta_credito_nombre = ""
        cuenta_credito_codigo = ""
        if instance.cuenta_credito:
            cuenta_credito_nombre = instance.cuenta_credito.nombre
            cuenta_credito_codigo = instance.cuenta_credito.codigo            
        return {
            'id': instance.id,         
            'tipo': instance.tipo,
            'orden': instance.orden,
            'tipo_costo_id': instance.tipo_costo_id,
            'tipo_costo_nombre': tipo_costo_nombre,
            'cuenta_debito_id': instance.cuenta_debito_id,
            'cuenta_debito_nombre': cuenta_debito_nombre,
            'cuenta_debito_codigo': cuenta_debito_codigo,
            'cuenta_credito_id': instance.cuenta_credito_id,
            'cuenta_credito_nombre': cuenta_credito_nombre,
            'cuenta_credito_codigo': cuenta_credito_codigo
        }              