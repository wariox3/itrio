from rest_framework import serializers
from vertical.models.estado import VerEstado

class VerEstadoSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerEstado
        fields = ['id', 'nombre']
        