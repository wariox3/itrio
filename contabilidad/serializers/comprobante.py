from rest_framework import serializers
from contabilidad.models.comprobante import ConComprobante

class ConComprobanteSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConComprobante
        fields = ['id', 'nombre', 'codigo', 'permite_asiento']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'codigo': instance.codigo,
            'permite_asiento' : instance.permite_asiento
        } 


class ConComprobanteListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConComprobante

    def to_representation(self, instance):
        return {
            'comprobante_id': instance.id,
            'comprobante_nombre': instance.nombre,
            'comprobante_codigo': instance.codigo
        }         
        