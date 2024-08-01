from general.models.precio_detalle import GenPrecioDetalle
from general.models.precio import GenPrecio
from general.models.item import GenItem
from rest_framework import serializers

class GenPrecioDetalleSerializador(serializers.HyperlinkedModelSerializer):
    precio = serializers.PrimaryKeyRelatedField(queryset=GenPrecio.objects.all())
    item = serializers.PrimaryKeyRelatedField(queryset=GenItem.objects.all(), allow_null=True)
    class Meta:
        model = GenPrecioDetalle
        fields = ['precio', 'vr_precio']

    def to_representation(self, instance):
        return {
            'id': instance.id,
        }        