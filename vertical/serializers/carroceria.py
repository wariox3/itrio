from rest_framework import serializers
from vertical.models.carroceria import VerCarroceria

class VerCarroceriaSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerCarroceria
        fields = ['id', 'nombre']
        