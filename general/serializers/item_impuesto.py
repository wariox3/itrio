from general.models.item_impuesto import ItemImpuesto
from general.models.item import Item
from general.models.impuesto import Impuesto
from rest_framework import serializers

class GenItemImpuestoSerializador(serializers.HyperlinkedModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    impuesto = serializers.PrimaryKeyRelatedField(queryset=Impuesto.objects.all())
    class Meta:
        model = ItemImpuesto
        fields = ['item', 'impuesto']

class GenItemImpuestoDetalleSerializador(serializers.HyperlinkedModelSerializer):
    impuesto = serializers.PrimaryKeyRelatedField(queryset=Impuesto.objects.all())
    class Meta:
        model = ItemImpuesto
        fields = ['item', 'impuesto']  

    def to_representation(self, instance):
        return {          
            'id': instance.id,
            'impuesto_id': instance.impuesto_id,
            'impuesto_nombre': instance.impuesto.nombre,
            'impuesto_nombre_extendido': instance.impuesto.nombre_extendido,
            'impuesto_porcentaje': instance.impuesto.porcentaje,
            'impuesto_porcentaje_base': instance.impuesto.porcentaje_base,
            'impuesto_venta': instance.impuesto.venta,
            'impuesto_compra': instance.impuesto.compra
        }          