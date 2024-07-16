from rest_framework import serializers
from ruteo.models.rut_despacho import RutDespacho


class RutDespachoSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = RutDespacho
        fields = ['id', 'peso', 'volumen', 'vehiculo']

    def to_representation(self, instance):        
        return {
            'id': instance.id,  
            'peso': instance.peso,
            'volumen': instance.volumen,
            'vehiculo_id': instance.vehiculo_id
        }
    
