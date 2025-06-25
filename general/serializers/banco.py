from general.models.banco import GenBanco
from rest_framework import serializers

class GenBancoSerializador(serializers.ModelSerializer):
    class Meta:
        model = GenBanco
        fields = ['id', 'nombre', 'codigo'] 