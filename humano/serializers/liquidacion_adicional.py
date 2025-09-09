from rest_framework import serializers
from humano.models.liquidacion_adicional import HumLiquidacionAdicional

class HumLiquidacionAdicionalSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumLiquidacionAdicional
        fields = ['id', 'adicional', 'deduccion', 'liquidacion']

