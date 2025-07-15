from rest_framework import serializers
from transporte.models.marca import TteMarca

class TteMarcaSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteMarca
        fields = ['id', 'nombre']

class TteMarcaSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteMarca
        fields = ['id', 'nombre']
