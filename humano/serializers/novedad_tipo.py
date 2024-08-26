from rest_framework import serializers
from humano.models.novedad_tipo import HumNovedadTipo
from humano.models.concepto import HumConcepto

class HumNovedadTipoSerializador(serializers.HyperlinkedModelSerializer):
    concepto = serializers.PrimaryKeyRelatedField(queryset=HumConcepto.objects.all())
    class Meta:
        model = HumNovedadTipo
        fields = ['id', 'nombre', 'concepto', 'concepto2', 'novedad_clase_id']

    def to_representation(self, instance):      

        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'concepto_id': instance.concepto_id,
            'concepto2_id': instance.concepto2_id,
            'novedad_clase_id': instance.novedad_clase_id
        }       

class HumNovedadTipoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumNovedadTipo

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'novedad_clase_id': instance.novedad_clase_id
        }        