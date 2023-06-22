from rest_framework import serializers
from general.models.movimiento import Movimiento
from general.models.movimiento_tipo import MovimientoTipo

class MovimientoSerializer(serializers.HyperlinkedModelSerializer):
    
    movimiento_tipo = serializers.PrimaryKeyRelatedField(queryset=MovimientoTipo.objects.all())
    
    class Meta:
        model = Movimiento
        fields = ['id', 'movimiento_tipo']
        