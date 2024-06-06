from rest_framework import serializers
from humano.models.hum_contrato import HumContrato

class HumContratoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumContrato
        fields = ['id']
        