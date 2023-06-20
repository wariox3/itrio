from general.models.item import Item
from general.models.impuesto import Impuesto
from general.models.item_impuesto import ItemImpuesto
from general.serializers.item_impuesto import ItemImpuestoSerializer
from rest_framework import serializers

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    itemImpuestos = ItemImpuestoSerializer(many=True)

    class Meta:
        model = Item
        fields = ['nombre', 'itemImpuestos']

    def create(self, validated_data):
        #item = Item(nombre=validated_data.get("nombre") )
        #item.save()        
        #itemImpuestos = validated_data.get('itemImpuestos')              
        #for itemImpuesto in itemImpuestos:
        #  impuesto = Impuesto.objects.get(id=itemImpuesto['impuesto_id'])
        #  ItemImpuesto.objects.create(item=item, impuesto=impuesto, **itemImpuesto)
        return validated_data   
    
    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.save()        
        ItemImpuesto.objects.filter(item_id=instance.id).delete()
        itemImpuestos = validated_data.get('itemImpuestos')
        for itemImpuesto in itemImpuestos:
          ItemImpuesto.objects.create(item=instance, **itemImpuesto)
        return validated_data  