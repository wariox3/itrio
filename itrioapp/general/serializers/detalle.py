from general.models.movimiento_detalle import MovimientoDetalle
from rest_framework import serializers

class DetalleSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = MovimientoDetalle
        fields = ['cantidad']