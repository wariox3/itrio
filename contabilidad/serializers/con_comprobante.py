from rest_framework import serializers
from contabilidad.models.con_comprobante import ConComprobante

class ConComprobanteSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConComprobante
        fields = ['id', 'nombre']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre
        } 


class ConComprobanteListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConComprobante

    def to_representation(self, instance):
        return {
            'comprobante_id': instance.id,
            'comprobante_nombre': instance.nombre
        }         
        