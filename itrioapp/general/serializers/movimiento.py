from general.models.movimiento import Movimiento
from rest_framework import serializers

class MovimientoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movimiento
        fields = ['id']