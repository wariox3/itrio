from rest_framework import serializers
from vertical.models.pais import VerPais

class VerPaisSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerPais
        fields = ['id', 'nombre']
        