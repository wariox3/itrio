from general.models.asesor import GenAsesor
from rest_framework import serializers

class GenAsesorSerializador(serializers.ModelSerializer):
    class Meta:
        model = GenAsesor
        fields = ['id','nombre_corto', 'celular','correo']       