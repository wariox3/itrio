from rest_framework import serializers
from general.models.movimiento import Movimiento
from general.models.detalle import Detalle
from general.serializers.detalle import DetalleSerializer



class MovimientoSerializer(serializers.HyperlinkedModelSerializer):
    detalles = DetalleSerializer(many=True)

    class Meta:
        model = Movimiento
        fields = ['id', 'detalles']

    def create(self, validated_data):
        movimiento = Movimiento()
        movimiento.save()        
        detalles = validated_data.get('detalles')
        for detalle in detalles:
          Detalle.objects.create(movimiento=movimiento, **detalle)
        return validated_data   
        