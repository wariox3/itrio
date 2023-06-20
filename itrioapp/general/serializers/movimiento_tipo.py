from rest_framework import serializers
from general.models.movimiento_tipo import MovimientoTipo

class MovimientoTipoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MovimientoTipo
        fields = ['id', 'nombre'] 
        