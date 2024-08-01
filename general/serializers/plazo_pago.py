from general.models.plazo_pago import GenPlazoPago
from rest_framework import serializers

class GenPlazoPagoSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenPlazoPago
        fields = ['id', 'nombre', 'dias']
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'dias': instance.dias
        }        
    
class GenPlazoPagoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenPlazoPago 
        
    def to_representation(self, instance):
        return {
            'plazo_pago_id': instance.id,            
            'plazo_pago_nombre': instance.nombre,
            'plazo_dias': instance.dias
        }     