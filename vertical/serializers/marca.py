from rest_framework import serializers
from vertical.models.marca import VerMarca

class VerMarcaSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerMarca
        fields = ['id', 'nombre']
        