from general.models.precio_detalle import GenPrecioDetalle
from rest_framework import serializers

class GenPrecioDetalleSerializador(serializers.ModelSerializer):
    item__nombre = serializers.CharField(source='item.nombre', read_only=True)

    class Meta:
        model = GenPrecioDetalle
        fields = ['id', 'precio', 'vr_precio', 'item', 'item__nombre']
        select_related_fields = ['item']