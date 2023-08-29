from general.models.forma_pago import FormaPago
from rest_framework import serializers

class FormaPagoSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FormaPago
        fields = ['id', 'nombre'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre
        }        
    
class FormaPagoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FormaPago 
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre
        }     