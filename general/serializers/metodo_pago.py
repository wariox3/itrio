from general.models.metodo_pago import MetodoPago
from rest_framework import serializers

class MetodoPagoSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MetodoPago
        fields = ['id', 'nombre']  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre
        }    

class MetodoPagoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MetodoPago 
        
    def to_representation(self, instance):
        return {
            'metodo_pago_id': instance.id,            
            'metodo_pogo_nombre': instance.nombre
        }           