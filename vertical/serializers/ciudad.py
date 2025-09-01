from rest_framework import serializers
from vertical.models.ciudad import VerCiudad

class VerCiudadSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerCiudad
        fields = ['id', 'nombre']

class VerCiudadSeleccionarSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerCiudad
        fields = ['id', 'nombre']        