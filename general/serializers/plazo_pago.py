from general.models.plazo_pago import PlazoPago
from rest_framework import serializers

class PlazoPagoSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlazoPago
        fields = ['id', 'nombre', 'dias']
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'dias': instance.dias
        }        
    
class PlazoPagoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlazoPago 
        
    def to_representation(self, instance):
        return {
            'plazo_pago_id': instance.id,            
            'plazo_pago_nombre': instance.nombre,
            'plazo_dias': instance.dias
        }     