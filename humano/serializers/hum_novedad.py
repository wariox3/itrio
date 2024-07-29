from rest_framework import serializers
from humano.models.hum_novedad import HumNovedad
from humano.models.hum_contrato import HumContrato

class HumNovedadSerializador(serializers.HyperlinkedModelSerializer):
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())
    
    class Meta:
        model = HumNovedad
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'contrato']
        