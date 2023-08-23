from rest_framework import serializers
from inquilino.models import Empresa, Plan, Consumo, Verificacion, UsuarioEmpresa, Movimiento
from seguridad.models import User
    
class ConsumoSerializador(serializers.ModelSerializer):
    class Meta:
        model = Consumo
        fields = ['empresa']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'empresa': instance.nombre,
        }   