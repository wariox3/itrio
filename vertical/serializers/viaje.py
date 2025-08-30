from rest_framework import serializers
from vertical.models.viaje import VerViaje

class VerViajeSerializador(serializers.ModelSerializer):
    class Meta:
        model = VerViaje
        fields = ['id', 'fecha', 'unidades', 'peso', 'volumen', 'negocio_id', 'contenedor_id', 'usuario', 'ciudad_origen', 'ciudad_destino', 'schema_name']


          
        