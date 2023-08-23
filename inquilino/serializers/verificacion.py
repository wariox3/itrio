from rest_framework import serializers
from inquilino.models import Empresa, Plan, Consumo, Verificacion, UsuarioEmpresa, Movimiento
from seguridad.models import User 

class VerificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verificacion
        fields = ['id', 'token', 'estado_usado', 'vence', 'accion', 'usuario_id', 'empresa_id', 'usuario_invitado_username']      