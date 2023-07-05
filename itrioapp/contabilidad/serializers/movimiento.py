from rest_framework import serializers
from contabilidad.models.movimiento import Movimiento

class MovimientoSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Movimiento
        fields = ['id']
        