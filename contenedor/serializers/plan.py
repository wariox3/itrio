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
            'limite_usuario': instance.limite_usuario,
            'limite_ingresos': instance.limite_ingresos,
            'precio': instance.precio,
            'limite_electronicos': instance.limite_electronicos
        }           