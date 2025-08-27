from rest_framework import serializers
from vertical.models.combustible import VerCombustible

class VerCombustibleSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerCombustible
        fields = ['id', 'nombre']
        