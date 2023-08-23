from rest_framework import serializers
from inquilino.models import Empresa, Plan, Consumo, Verificacion, UsuarioEmpresa, Movimiento
from seguridad.models import User       

class PlanSerializador(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['nombre']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }           