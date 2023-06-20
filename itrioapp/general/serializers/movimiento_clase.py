from rest_framework import serializers
from general.models.movimiento_clase import MovimientoClase

class MovimientoClaseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MovimientoClase
        fields = ['id', 'nombre'] 
        