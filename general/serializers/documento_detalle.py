from general.models.documento_detalle import DocumentoDetalle
from general.models.documento import Documento
from general.models.item import Item
from rest_framework import serializers

class DocumentoDetalleSerializador(serializers.HyperlinkedModelSerializer):
    documento = serializers.PrimaryKeyRelatedField(queryset=Documento.objects.all())
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), default=None, allow_null=True)
    documento_afectado = serializers.PrimaryKeyRelatedField(queryset=Documento.objects.all(), default=None, allow_null=True)
    class Meta:
        model = DocumentoDetalle
        fields = ['documento', 'documento_afectado', 'item', 'cantidad', 'precio', 'porcentaje_descuento', 'descuento', 'subtotal', 'total_bruto', 'total']

    def to_representation(self, instance):
        item = instance.item
        item_nombre = ""
        if item is not None:
            item_nombre = item.nombre
        return {
            'id': instance.id,            
            'documento_id': instance.documento_id,
            'documento_afectado_id': instance.documento_afectado_id,
            'item': instance.item_id,
            'item_nombre': item_nombre,
            'cantidad': instance.cantidad,
            'precio': instance.precio,
            'porcentaje_descuento': instance.porcentaje_descuento,
            'descuento' :  instance.descuento,
            'subtotal' : instance.subtotal,
            'total_bruto' : instance.total_bruto,
            'total' : instance.total
        }        