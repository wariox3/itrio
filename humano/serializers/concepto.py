from rest_framework import serializers
from humano.models.concepto import HumConcepto

class HumConceptoSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumConcepto
        fields = ['id', 'nombre', 'porcentaje', 'ingreso_base_prestacion', 'ingreso_base_prestacion_vacacion', 'ingreso_base_cotizacion', 
                  'orden', 'adicional', 'concepto_tipo']

    def to_representation(self, instance):
        concepto_tipo_nombre = ''
        if instance.concepto_tipo:
            concepto_tipo_nombre = instance.concepto_tipo.nombre        
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'porcentaje': instance.porcentaje,
            'ingreso_base_cotizacion': instance.ingreso_base_cotizacion,
            'ingreso_base_prestacion': instance.ingreso_base_prestacion,
            'ingreso_base_prestacion_vacacion': instance.ingreso_base_prestacion_vacacion,
            'adicional': instance.adicional,
            'orden': instance.orden,            
            'concepto_tipo_id': instance.concepto_tipo_id,
            'concepto_tipo_nombre': concepto_tipo_nombre
        } 
class HumConceptoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumConcepto

    def to_representation(self, instance):
        return {
            'concepto_id': instance.id,
            'concepto_nombre': instance.nombre,
        }         
        