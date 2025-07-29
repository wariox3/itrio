from contenedor.models import CtnIdentificacion
from rest_framework import serializers

class CtnIdentificacionSerializador(serializers.ModelSerializer):
    class Meta:
        model = CtnIdentificacion
        fields = ['id', 'nombre']  
        
class CtnIdentificacionSeleccionarSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = CtnIdentificacion
        fields = ['id', 'nombre']  