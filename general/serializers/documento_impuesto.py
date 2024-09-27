from general.models.documento_impuesto import GenDocumentoImpuesto
from general.models.documento_detalle import GenDocumentoDetalle
from general.models.impuesto import GenImpuesto
from rest_framework import serializers

class GenDocumentoImpuestoSerializador(serializers.HyperlinkedModelSerializer):
    documento_detalle = serializers.PrimaryKeyRelatedField(queryset=GenDocumentoDetalle.objects.all())
    impuesto = serializers.PrimaryKeyRelatedField(queryset=GenImpuesto.objects.all())
    class Meta:
        model = GenDocumentoImpuesto
        fields = ['documento_detalle', 'impuesto', 'base', 'porcentaje', 'total', 'total_operado', 'porcentaje_base']
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'impuesto_id': instance.impuesto_id,
            'impuesto_nombre': instance.impuesto.nombre,
            'impuesto_nombre_extendido': instance.impuesto.nombre_extendido,
            'impuesto_porcentaje': instance.impuesto.porcentaje,
            'impuesto_porcentaje_base': instance.impuesto.porcentaje_base,
            'impuesto_venta': instance.impuesto.venta,
            'impuesto_compra': instance.impuesto.compra,
            'base': instance.base,
            'porcentaje': instance.porcentaje,
            'total': instance.total,
            'total_operado': instance.total_operado
        }         