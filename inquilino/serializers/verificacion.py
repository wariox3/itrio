from rest_framework import serializers
from inquilino.models import Verificacion

class VerificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verificacion
        fields = ['id', 'token', 'estado_usado', 'vence', 'accion', 'usuario_id', 'inquilino_id', 'usuario_invitado_username']      