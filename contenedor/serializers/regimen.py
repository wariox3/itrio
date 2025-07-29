from contenedor.models import CtnRegimen
from rest_framework import serializers

class CtnRegimenSerializador(serializers.ModelSerializer):
    class Meta:
        model = CtnRegimen
        fields = [
            'id', 
            'nombre'
            ]  
             

class CtnRegimenSeleccionarSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = CtnRegimen
        fields = [
            'id', 
            'nombre'
            ]