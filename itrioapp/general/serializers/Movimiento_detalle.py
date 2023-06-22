from general.models.movimiento_detalle import MovimientoDetalle
from general.models.movimiento import Movimiento
from general.models.item import Item
from rest_framework import serializers

class MovimientoDetalleSerializer(serializers.HyperlinkedModelSerializer):
    movimiento = serializers.PrimaryKeyRelatedField(queryset=Movimiento.objects.all())
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    class Meta:
        model = MovimientoDetalle
        fields = ['movimiento', 'item', 'cantidad']