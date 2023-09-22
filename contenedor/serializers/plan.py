from rest_framework import serializers
from contenedor.models import Plan       

class PlanSerializador(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['nombre']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }           