from rest_framework import serializers
from contenedor.models import Verificacion

class VerificacionSerializador(serializers.ModelSerializer):
    class Meta:
        model = Verificacion
        fields = ['id', 'token', 'estado_usado', 'vence', 'accion', 'usuario_id', 'contenedor_id', 'usuario_invitado_username']      