from rest_framework import serializers
from contabilidad.models.movimiento import ConMovimiento

class MovimientoSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConMovimiento
        fields = ['id']
        