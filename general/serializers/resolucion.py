from rest_framework import serializers
from general.models.resolucion import Resolucion

class ResolucionSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Resolucion
        fields = ['id', 'prefijo', 'numero', 'consecutivo_desde', 'consecutivo_hasta', 'fecha_desde', 'fecha_hasta', 'venta', 'compra'] 

class ResolucionListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Resolucion

    def to_representation(self, instance):
        return {
            'resolucion_id': instance.id,            
            'resolucion_numero': instance.numero,
            'resolucion_prefijo': instance.prefijo
        }       
        