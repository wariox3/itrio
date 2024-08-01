from general.models.forma_pago import FormaPago
from rest_framework import serializers

class GenFormaPagoSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FormaPago
        fields = ['id', 'nombre'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre
        }        
    
class GenFormaPagoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FormaPago 
        
    def to_representation(self, instance):
        return {
            'forma_pago_id': instance.id,            
            'forma_pago_nombre': instance.nombre
        }     