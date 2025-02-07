from rest_framework import serializers
from general.models.impuesto import GenImpuesto
from general.models.impuesto_tipo import GenImpuestoTipo
from contabilidad.models.cuenta import ConCuenta

class GenImpuestoSerializador(serializers.HyperlinkedModelSerializer):
    impuesto_tipo = serializers.PrimaryKeyRelatedField(queryset=GenImpuestoTipo.objects.all(), default=None, allow_null=True)
    cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    class Meta:
        model = GenImpuesto
        fields = ['nombre', 'nombre_extendido', 'porcentaje', 'impuesto_tipo', 'cuenta']

    def to_representation(self, instance):
      cuenta_nombre = ''
      if instance.cuenta:
          cuenta_nombre = instance.cuenta.nombre
      return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'nombre_extendido' : instance.nombre_extendido,
            'porcentaje': instance.porcentaje,
            'operacion': instance.operacion,
            'cuenta_id': instance.cuenta_id,
            'cuenta_nombre': cuenta_nombre
        }         

class GenImpuestoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenImpuesto

    def to_representation(self, instance):
        return {
            'impuesto_id': instance.id,            
            'impuesto_nombre': instance.nombre,
            'impuesto_nombre_extendido': instance.nombre_extendido,
            'impuesto_porcentaje': instance.porcentaje,
            'impuesto_compra': instance.compra,
            'impuesto_venta': instance.venta,
            'impuesto_porcentaje_base': instance.porcentaje_base,
            'impuesto_operacion': instance.operacion
        }             