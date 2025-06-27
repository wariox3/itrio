from general.models.precio import GenPrecio
from rest_framework import serializers

class GenPrecioSerializador(serializers.ModelSerializer):          
    class Meta:
        model = GenPrecio
        fields = ['id', 
                  'nombre',
                  'fecha_vence']

class GenPrecioSeleccionarSerializador(serializers.ModelSerializer):          
    class Meta:
        model = GenPrecio
        fields = ['id', 
                  'nombre']