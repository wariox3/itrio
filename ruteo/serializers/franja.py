from rest_framework import serializers
from ruteo.models.franja import RutFranja


class RutFranjaSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = RutFranja
        fields = ['id', 'nombre', 'coordenadas']

    def to_representation(self, instance):        
        return {
            'id': instance.id,  
            'nombre': instance.nombre,
            'coordenadas': instance.coordenadas
        }
    
