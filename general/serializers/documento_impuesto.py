from general.models.documento_impuesto import DocumentoImpuesto
from general.models.documento_detalle import DocumentoDetalle
from general.models.impuesto import Impuesto
from rest_framework import serializers

class DocumentoImpuestoSerializador(serializers.HyperlinkedModelSerializer):
    documento_detalle = serializers.PrimaryKeyRelatedField(queryset=DocumentoDetalle.objects.all())
    impuesto = serializers.PrimaryKeyRelatedField(queryset=Impuesto.objects.all())
    class Meta:
        model = DocumentoImpuesto
        fields = ['documento_detalle', 'impuesto', 'base', 'porcentaje', 'total', 'porcentaje_base']
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'impuesto_id': instance.impuesto_id,
            'impuesto_nombre': instance.impuesto.nombre,
            'impuesto_nombre_extendido': instance.impuesto.nombre_extendido,
            'impuesto_porcentaje': instance.impuesto.porcentaje,
            'impuesto_porcentaje_base': instance.impuesto.porcentaje_base,
            'base': instance.base,
            'porcentaje': instance.porcentaje,
            'total': instance.total,
        }         