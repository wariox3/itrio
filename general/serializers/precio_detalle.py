from general.models.precio_detalle import PrecioDetalle
from general.models.precio import Precio
from general.models.item import Item
from rest_framework import serializers

class GenPrecioDetalleSerializador(serializers.HyperlinkedModelSerializer):
    precio = serializers.PrimaryKeyRelatedField(queryset=Precio.objects.all())
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), allow_null=True)
    class Meta:
        model = PrecioDetalle
        fields = ['precio', 'vr_precio']

    def to_representation(self, instance):
        return {
            'id': instance.id,
        }        