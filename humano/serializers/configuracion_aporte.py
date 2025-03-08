from rest_framework import serializers
from humano.models.configuracion_aporte import HumConfiguracionAporte
from contabilidad.models.cuenta import ConCuenta

class HumConfiguracionAporteSerializador(serializers.HyperlinkedModelSerializer):
    cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)

    class Meta:
        model = HumConfiguracionAporte
        fields = ['id', 'tipo', 'orden', 'cuenta']    

    def to_representation(self, instance):       
        cuenta_nombre = ""
        cuenta_codigo = ""
        if instance.cuenta:
            cuenta_nombre = instance.cuenta.nombre
            cuenta_codigo = instance.cuenta.codigo            
        return {
            'id': instance.id,         
            'tipo': instance.tipo,
            'orden': instance.orden,
            'cuenta_id': instance.cuenta_id,
            'cuenta_codigo': cuenta_codigo,
            'cuenta_nombre': cuenta_nombre
        }              