from rest_framework import serializers
from contenedor.models import CtnInvitacion
from seguridad.models import User
from datetime import datetime
from decouple import config

class CntInvitacionSerializador(serializers.ModelSerializer):

    class Meta:
        model = CtnInvitacion
        fields = ['id', 'fecha', 'usuario_invitado', 'usuario','contenedor']             