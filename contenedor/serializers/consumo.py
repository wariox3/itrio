from rest_framework import serializers
from contenedor.models import CtnConsumo
    
class CtnSerializador(serializers.ModelSerializer):
    class Meta:
        model = CtnConsumo
        fields = ['contenedor']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'contenedor': instance.nombre,
        }   