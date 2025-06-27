from rest_framework import serializers
from humano.models.tipo_cotizante import HumTipoCotizante

class HumTipoCotizanteSeleccionarSerializador(serializers.ModelSerializer):
    class Meta:
        model = HumTipoCotizante
        fields = ['id', 'nombre']

class HumTipoCotizanteSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumTipoCotizante
        fields = ['id', 'nombre']

class HumTipoCotizanteListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumTipoCotizante

    def to_representation(self, instance):
        return {
            'tipo_cotizante_id': instance.id,
            'tipo_cotizante_nombre': instance.nombre,
        }          