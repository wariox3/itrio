from rest_framework import serializers
from general.models.impuesto_tipo import GenImpuestoTipo

class GenImpuestoTipoSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GenImpuestoTipo
        fields = ['id', 'codigo','nombre']

    def to_representation(self, instance):
      return {
            'id': instance.id,            
            'codigo': instance.codigo,
            'nombre': instance.nombre
        }         
            