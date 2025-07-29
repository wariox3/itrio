from contenedor.models import CtnCiudad
from rest_framework import serializers

class CtnCiudadSerializador(serializers.ModelSerializer):
    estado__nombre = serializers.CharField(source='estado.nombre', read_only=True)
    class Meta:
        model = CtnCiudad
        fields = ['id', 'nombre', 'estado__nombre']  
        select_related_fields = ['estado']        
        
     
class CtnCiudadSeleccionarSerializador(serializers.ModelSerializer):
    estado__nombre = serializers.CharField(source='estado.nombre', read_only=True)
    class Meta:
        model = CtnCiudad
        fields = ['id', 'nombre', 'estado__nombre']  
        select_related_fields = ['estado']    