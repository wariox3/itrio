from contenedor.models import CtnTipoPersona
from rest_framework import serializers

class CtnTipoPersonaSerializador(serializers.ModelSerializer):
    class Meta:
        model = CtnTipoPersona
        fields = [
            'id', 
            'nombre'
            ]  
             

class CtnTipoPersonaSeleccionarSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = CtnTipoPersona
        fields = [
            'id', 
            'nombre'
            ]  