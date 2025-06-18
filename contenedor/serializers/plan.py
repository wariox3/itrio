from rest_framework import serializers
from contenedor.models import CtnPlan       


class CtnPlanListaSerializador(serializers.ModelSerializer):          
    class Meta:
        model = CtnPlan
        fields = ['id', 
                  'nombre']

class CtnPlanSerializador(serializers.ModelSerializer):
    class Meta:
        model = CtnPlan
        fields = ['nombre']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'limite_usuarios': instance.limite_usuarios,
            'limite_ingresos': instance.limite_ingresos,
            'precio': instance.precio,
            'limite_electronicos': instance.limite_electronicos,
            'plan_tipo_id': instance.plan_tipo_id
        }           