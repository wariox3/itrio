from rest_framework import serializers
from humano.models.hum_adicional import HumAdicional

class HumAdicionalSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumAdicional
        fields = ['id']
        