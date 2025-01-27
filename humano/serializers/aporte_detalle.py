from rest_framework import serializers
from humano.models.aporte_detalle import HumAporteDetalle
from humano.models.aporte_contrato import HumAporteContrato

class HumAporteDetalleSerializador(serializers.HyperlinkedModelSerializer):    
    aporte_contrato = serializers.PrimaryKeyRelatedField(queryset=HumAporteContrato.objects.all())

    class Meta:
        model = HumAporteDetalle
        fields = ['id']            