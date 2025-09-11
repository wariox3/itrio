from rest_framework import serializers
from humano.models.liquidacion_adicional import HumLiquidacionAdicional

class HumLiquidacionAdicionalSerializador(serializers.ModelSerializer):
    concepto__nombre = serializers.CharField(source='concepto.nombre', read_only=True)
    class Meta:
        model = HumLiquidacionAdicional
        fields = ['id', 'adicional', 'deduccion', 'liquidacion', 'concepto', 'concepto__nombre']
        select_related_fields = ['concepto']

