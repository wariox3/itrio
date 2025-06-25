from general.models.identificacion import GenIdentificacion
from rest_framework import serializers

class GenIdentificacionSerializador(serializers.ModelSerializer):
    class Meta:
        model = GenIdentificacion
        fields = ['id', 'nombre', 'tipo_persona']        