from rest_framework import serializers
from vertical.models.viaje import VerViaje

class VerViajeSerializador(serializers.ModelSerializer):
    class Meta:
        model = VerViaje
        fields = ['id', 'fecha', 'unidades', 'peso', 'volumen', 'negocio_id', 'contenedor_id', 'schema_name', 'solicitud_cliente', 
                  'estado_aceptado', 'flete', 
                  'vehiculo', 
                  'conductor',
                  'usuario', 
                  'ciudad_origen', 
                  'ciudad_destino']        

class VerViajeListaSerializador(serializers.ModelSerializer):
    class Meta:
        model = VerViaje
        fields = ['id']          
        