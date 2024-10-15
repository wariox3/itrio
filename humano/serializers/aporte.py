from rest_framework import serializers
from humano.models.aporte import HumAporte
from humano.models.sucursal import HumSucursal

class HumAporteSerializador(serializers.HyperlinkedModelSerializer):
    sucursal = serializers.PrimaryKeyRelatedField(queryset=HumSucursal.objects.all())

    class Meta:
        model = HumAporte
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'sucursal']        