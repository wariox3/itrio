from rest_framework import serializers
from general.models.impuesto import Impuesto

class ImpuestoSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Impuesto
        fields = ['nombre']

    def to_representation(self, instance):
      return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'nombre_extendido' : instance.nombre_extendido,
            'porcentaje': instance.porcentaje
        }         

class ImpuestoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Impuesto

    def to_representation(self, instance):
        return {
            'impuesto_id': instance.id,            
            'impuesto_nombre': instance.nombre,
            'impuesto_nombre_extendido': instance.nombre_extendido,
            'impuesto_porcentaje': instance.porcentaje,
            'impuesto_compra': instance.compra,
            'impuesto_venta': instance.venta,
            'impuesto_porcentaje_base': instance.porcentaje_base,
        }             