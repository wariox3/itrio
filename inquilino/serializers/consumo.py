from rest_framework import serializers
from inquilino.models import Consumo
    
class ConsumoSerializador(serializers.ModelSerializer):
    class Meta:
        model = Consumo
        fields = ['inquilino']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'inquilino': instance.nombre,
        }   