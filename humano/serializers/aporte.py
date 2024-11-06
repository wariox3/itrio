from rest_framework import serializers
from humano.models.aporte import HumAporte
from humano.models.sucursal import HumSucursal

class HumAporteSerializador(serializers.HyperlinkedModelSerializer):
    anio = serializers.IntegerField(required=True)
    mes = serializers.IntegerField(required=True)    
    sucursal = serializers.PrimaryKeyRelatedField(queryset=HumSucursal.objects.all())

    class Meta:
        model = HumAporte
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'fecha_hasta_periodo', 'anio', 'mes', 'anio_salud', 'mes_salud', 'sucursal']        