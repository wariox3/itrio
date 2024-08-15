from rest_framework import serializers
from humano.models.riesgo import HumRiesgo

class HumRiesgoSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumRiesgo
        fields = ['id', 'codigo', 'nombre', 'porcentaje']

    

class HumRiesgoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumRiesgo

    def to_representation(self, instance):
        return {
            'riesgo_id': instance.id,
            'riesgo_codigo': instance.codigo,
            'riesgo_nombre': instance.nombre,
            'riesgo_porcenjate': instance.porcentaje,
        }         
        