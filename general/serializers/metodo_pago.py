from general.models.metodo_pago import GenMetodoPago
from rest_framework import serializers

class GenMetodoPagoSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenMetodoPago
        fields = ['id', 'nombre']  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre
        }    

class GenMetodoPagoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenMetodoPago 
        
    def to_representation(self, instance):
        return {
            'metodo_pago_id': instance.id,            
            'metodo_pogo_nombre': instance.nombre
        }           