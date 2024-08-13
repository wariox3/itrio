from rest_framework import serializers
from transporte.models.guia import TteGuia


class TteGuiaSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = TteGuia
        fields = ['id']

    def to_representation(self, instance):        
        return {
            'id': instance.id,            
        }
    
