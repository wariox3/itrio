from rest_framework import serializers
from general.models.impuesto import GenImpuesto
from general.models.impuesto_tipo import GenImpuestoTipo
from contabilidad.models.cuenta import ConCuenta

class GenImpuestoSerializador(serializers.HyperlinkedModelSerializer):    
    cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    class Meta:
        model = GenImpuesto
        fields = ['id', 'cuenta']

    def to_representation(self, instance):
      cuenta_nombre = ''
      cuenta_codigo = ''
      if instance.cuenta:
          cuenta_nombre = instance.cuenta.nombre
          cuenta_codigo = instance.cuenta.codigo
      return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'nombre_extendido' : instance.nombre_extendido,
            'porcentaje': instance.porcentaje,
            'operacion': instance.operacion,
            'compra': instance.compra,
            'venta': instance.venta,
            'cuenta_id': instance.cuenta_id,
            'cuenta_nombre': cuenta_nombre,
            'cuenta_codigo' : cuenta_codigo
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

class GenImpuestoSeleccionarSerializador(serializers.ModelSerializer):
    class Meta:
        model = GenImpuesto
        fields = ['id', 'nombre', 'nombre_extendido', 'porcentaje', 'operacion', 'compra', 'venta', 'porcentaje_base']

    def to_representation(self, instance):
        return {
            'impuesto_id': instance.id,            
            'impuesto_nombre': instance.nombre,
            'impuesto_nombre_extendido': instance.nombre_extendido,
            'impuesto_porcentaje': instance.porcentaje,
            'impuesto_compra': instance.compra,
            'impuesto_venta': instance.venta,
            'impuesto_porcentaje_base': instance.porcentaje_base,
            'impuesto_operacion': instance.operacion,
            'impuesto_impuesto_tipo_id': instance.impuesto_tipo_id
        }