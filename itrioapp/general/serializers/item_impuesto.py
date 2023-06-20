from general.models.item_impuesto import ItemImpuesto
from rest_framework import serializers

class ItemImpuestoSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ItemImpuesto
        fields = ['impuesto_id']