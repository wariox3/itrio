from general.models.detalle import Detalle
from rest_framework import serializers

class DetalleSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Detalle
        fields = ['cantidad']