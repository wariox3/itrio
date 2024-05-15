from rest_framework import serializers
from transporte.models.guia import Guia


class GuiaSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = Guia
        fields = ['id']

    def to_representation(self, instance):        
        return {
            'id': instance.id,            
        }
    
