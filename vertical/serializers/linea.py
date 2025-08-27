from rest_framework import serializers
from vertical.models.linea import VerLinea

class VerLineaSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerLinea
        fields = ['id', 'nombre']
        