from rest_framework import serializers
from vertical.models.ciudad import VerCiudad

class VerCiudadSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerCiudad
        fields = ['id', 'nombre']

class VerCiudadSeleccionarSerializador(serializers.ModelSerializer):
    estado__nombre = serializers.CharField(source='estado.nombre', read_only=True)
    class Meta:
        model = VerCiudad
        fields = ['id', 'nombre', 'estado__nombre']  
        select_related_fields = ['estado']      