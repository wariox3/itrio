from rest_framework import serializers
from general.models.rh import GenRh

class GenRhSerializador(serializers.ModelSerializer):    
    class Meta:
        model = GenRh
        fields = ['id', 'nombre']

class GenRhSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = GenRh
        fields = ['id', 'nombre']
