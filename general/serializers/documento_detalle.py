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
        fields = ['documento', 'documento_afectado', 'item', 'cantidad', 'precio', 'porcentaje_descuento', 'descuento', 'subtotal', 'total_bruto', 'total', 'base_impuesto', 'impuesto']

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
            'base_impuesto' : instance.base_impuesto,
            'impuesto' : instance.impuesto,
            'total' : instance.total
        }  

class DocumentoDetalleInformeSerializador(serializers.HyperlinkedModelSerializer):
    documento = serializers.PrimaryKeyRelatedField(queryset=Documento.objects.all())
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), default=None, allow_null=True)
    documento_afectado = serializers.PrimaryKeyRelatedField(queryset=Documento.objects.all(), default=None, allow_null=True)
    class Meta:
        model = DocumentoDetalle
        fields = ['documento', 'documento_afectado', 'item', 'cantidad', 'precio', 'porcentaje_descuento', 'descuento', 'subtotal', 'total_bruto', 'total', 'base_impuesto', 'impuesto']

    def to_representation(self, instance):
        item = instance.item
        item_nombre = ""
        if item is not None:
            item_nombre = item.nombre
        documento = instance.documento
        documento_tipo_nombre = ""
        if documento is not None:
            documento_tipo = documento.documento_tipo
            if documento_tipo is not None:
                documento_tipo_nombre = documento_tipo.nombre
        return {
            'id': instance.id,            
            'documento_id': instance.documento_id,
            'dodumento_tipo_nombre': documento_tipo_nombre,        
            'fecha': documento.fecha,
            'numero': documento.numero,    
            'item': instance.item_id,
            'item_nombre': item_nombre,
            'cantidad': instance.cantidad,
            'precio': instance.precio,
            'porcentaje_descuento': instance.porcentaje_descuento,
            'descuento' :  instance.descuento,
            'subtotal' : instance.subtotal,
            'total_bruto' : instance.total_bruto,
            'base_impuesto' : instance.base_impuesto,
            'impuesto' : instance.impuesto,
            'total' : instance.total,
            'documento_afectado_id': instance.documento_afectado_id
        }           