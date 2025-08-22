from rest_framework import serializers
from transporte.models.categoria_licencia import TteCategoriaLicencia

class TteCategoriaLicenciaSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteCategoriaLicencia
        fields = ['id', 'nombre']

class TteCategoriaLicenciaSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteCategoriaLicencia
        fields = ['id', 'nombre']
