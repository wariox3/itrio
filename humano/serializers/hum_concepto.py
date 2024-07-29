from rest_framework import serializers
from humano.models.hum_concepto import HumConcepto

class HumConceptoSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumConcepto
        fields = ['id', 'nombre', 'porcentaje', 'ingreso_base_prestacion', 'ingreso_base_cotizacion', 'orden']
        