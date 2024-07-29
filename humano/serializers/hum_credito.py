from rest_framework import serializers
from humano.models.hum_credito import HumCredito
from humano.models.hum_contrato import HumContrato

class HumCreditoSerializador(serializers.HyperlinkedModelSerializer):
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())

    class Meta:
        model = HumCredito
        fields = ['id', 'fecha_inicio', 'total', 'cuota', 'cantidad_cuotas', 'validar_cuotas', 'contrato']
        