from rest_framework import serializers
from humano.models.subtipo_cotizante import HumSubtipoCotizante

class HumSubtipoCotizanteSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumSubtipoCotizante
        fields = ['id', 'nombre']

class HumSubtipoCotizanteListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumSubtipoCotizante

    def to_representation(self, instance):
        return {
            'subtipo_cotizante_id': instance.id,
            'subtipo_cotizante_nombre': instance.nombre,
        }          