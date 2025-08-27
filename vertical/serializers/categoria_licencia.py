from rest_framework import serializers
from vertical.models.categoria_licencia import VerCategoriaLicencia

class VerCategoriaLicenciaSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerCategoriaLicencia
        fields = ['id', 'nombre']
        