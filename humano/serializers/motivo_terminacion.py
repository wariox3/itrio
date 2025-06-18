from rest_framework import serializers
from humano.models.motivo_terminacion import HumMotivoTerminacion

class HumMotivoTerminacionSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HumMotivoTerminacion
        fields = ['id', 'nombre']        

class HumLiquidacionListaSerializador(serializers.HyperlinkedModelSerializer):      

    class Meta:
        model = HumMotivoTerminacion
        fields = ['id', 
                  'nombre']      
       
        