from general.models.documento_detalle import DocumentoDetalle
from general.models.documento import Documento
from general.models.item import Item
from rest_framework import serializers

class DocumentoDetalleSerializer(serializers.HyperlinkedModelSerializer):
    documento = serializers.PrimaryKeyRelatedField(queryset=Documento.objects.all())
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    class Meta:
        model = DocumentoDetalle
        fields = ['documento', 'item', 'cantidad', 'precio', 'porcentaje_descuento', 'descuento', 'subtotal', 'total_bruto', 'total']