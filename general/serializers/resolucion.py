from rest_framework import serializers
from general.models.resolucion import GenResolucion

class GenResolucionSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GenResolucion
        fields = ['id', 'prefijo', 'numero', 'consecutivo_desde', 'consecutivo_hasta', 'fecha_desde', 'fecha_hasta', 'venta', 'compra'] 

class GenResolucionListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenResolucion

    def to_representation(self, instance):
        return {
            'resolucion_id': instance.id,            
            'resolucion_numero': instance.numero,
            'resolucion_prefijo': instance.prefijo
        }       
        