from rest_framework import serializers
from humano.models.hum_concepto import HumConcepto

class HumConceptoSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumConcepto
        fields = ['id', 'nombre', 'porcentaje', 'ingreso_base_prestacion', 'ingreso_base_cotizacion', 'orden']

class HumConceptoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumConcepto

    def to_representation(self, instance):
        return {
            'concepto_id': instance.id,
            'nombre_nombre': instance.nombre,
        }         
        