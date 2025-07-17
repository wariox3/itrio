from rest_framework import serializers
from transporte.models.producto import TteProducto

class TteProductoSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteProducto
        fields = ['id', 'nombre']

class TteProductoSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteProducto
        fields = ['id', 'nombre']
