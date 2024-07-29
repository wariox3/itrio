from rest_framework import serializers
from humano.models.hum_adicional import HumAdicional
from humano.models.hum_contrato import HumContrato
from humano.models.hum_concepto import HumConcepto

class HumAdicionalSerializador(serializers.HyperlinkedModelSerializer):
    concepto = serializers.PrimaryKeyRelatedField(queryset=HumConcepto.objects.all())
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())

    class Meta:
        model = HumAdicional
        fields = ['id', 'valor', 'horas', 'aplica_dia_laborado', 'detalle', 'concepto', 'contrato']
        