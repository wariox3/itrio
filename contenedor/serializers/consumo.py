from rest_framework import serializers
from contenedor.models import Consumo
    
class ConsumoSerializador(serializers.ModelSerializer):
    class Meta:
        model = Consumo
        fields = ['contenedor']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'contenedor': instance.nombre,
        }   