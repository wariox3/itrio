from contenedor.models import CtnTipoPersona
from rest_framework import serializers

class CtnTipoPersonaSerializador(serializers.ModelSerializer):
    class Meta:
        model = CtnTipoPersona
        fields = [
            'id', 
            'nombre'
            ]  
             

class CtnTipoPersonaSeleccionarSerializadorSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = CtnTipoPersona
        fields = [
            'id', 
            'nombre'
            ]  