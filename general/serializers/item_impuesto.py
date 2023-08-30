from general.models.item_impuesto import ItemImpuesto
from general.models.item import Item
from general.models.impuesto import Impuesto
from rest_framework import serializers

class ItemImpuestoSerializador(serializers.HyperlinkedModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    impuesto = serializers.PrimaryKeyRelatedField(queryset=Impuesto.objects.all())
    class Meta:
        model = ItemImpuesto
        fields = ['item', 'impuesto']