from rest_framework import serializers
from vertical.models.producto import VerProducto

class VerProductoSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerProducto
        fields = ['id', 'nombre', 'codigo']

class VerProductoSeleccionarSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerProducto
        fields = ['id', 'nombre', 'codigo']        
        