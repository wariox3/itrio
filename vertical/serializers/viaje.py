from rest_framework import serializers
from vertical.models.viaje import VerViaje

class VerViajeSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VerViaje
        fields = ['id', 'fecha', 'peso', 'volumen', 'negocio_id', 'contenedor_id', 'usuario_id', 'schema_name']


          
        