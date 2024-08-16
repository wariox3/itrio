from rest_framework import serializers
from humano.models.concepto_nomina import HumConceptoNomina
from humano.models.concepto import HumConcepto

class HumConceptoNominaSerializador(serializers.HyperlinkedModelSerializer):
    concepto = serializers.PrimaryKeyRelatedField(queryset=HumConcepto.objects.all(), default=None, allow_null=True)
    class Meta:
        model = HumConceptoNomina
        fields = ['id', 'nombre', 'concepto']

        