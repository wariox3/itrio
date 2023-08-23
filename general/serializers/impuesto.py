from rest_framework import serializers
from general.models.impuesto import Impuesto

class ImpuestoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Impuesto
        fields = ['nombre']

    def to_representation(self, instance):
      return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'nombre_extendido' : instance.nombre_extendido,
            'porcentaje': instance.porcentaje
        }         
        