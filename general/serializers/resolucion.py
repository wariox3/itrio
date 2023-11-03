from rest_framework import serializers
from general.models.resolucion import Resolucion

class ResolucionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Resolucion
        fields = ['id', 'prefijo', 'numero', 'consecutivo_desde', 'consecutivo_hasta', 'fecha_desde', 'fecha_hasta'] 
        