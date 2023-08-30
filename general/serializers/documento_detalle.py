from general.models.documento_detalle import DocumentoDetalle
from general.models.documento import Documento
from general.models.item import Item
from rest_framework import serializers

class DocumentoDetalleSerializador(serializers.HyperlinkedModelSerializer):
    documento = serializers.PrimaryKeyRelatedField(queryset=Documento.objects.all())
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), allow_null=True)
    class Meta:
        model = DocumentoDetalle
        fields = ['documento', 'item', 'cantidad', 'precio', 'porcentaje_descuento', 'descuento', 'subtotal', 'total_bruto', 'total']

    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'documento': instance.documento_id,
            'item': instance.item_id,
            'item_nombre': instance.item.nombre,
            'cantidad': instance.cantidad,
            'precio': instance.precio,
            'porcentaje_descuento': instance.porcentaje_descuento,
            'descuento' :  instance.descuento,
            'subtotal' : instance.subtotal,
            'total_bruto' : instance.total_bruto,
            'total' : instance.total
        }        