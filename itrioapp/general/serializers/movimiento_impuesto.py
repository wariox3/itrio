from general.models.movimiento_impuesto import MovimientoImpuesto
from general.models.movimiento_detalle import MovimientoDetalle
from general.models.impuesto import Impuesto
from rest_framework import serializers

class MovimientoImpuestoSerializer(serializers.HyperlinkedModelSerializer):
    movimiento_detalle = serializers.PrimaryKeyRelatedField(queryset=MovimientoDetalle.objects.all())
    impuesto = serializers.PrimaryKeyRelatedField(queryset=Impuesto.objects.all())
    class Meta:
        model = MovimientoImpuesto
        fields = ['movimiento_detalle', 'impuesto', 'base', 'porcentaje', 'total']