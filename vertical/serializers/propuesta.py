from rest_framework import serializers
from vertical.models.propuesta import VerPropuesta

class VerPropuestaSerializador(serializers.ModelSerializer):
    class Meta:
        model = VerPropuesta
        fields = ['id', 'precio', 'pago', 'contenedor_id', 'schema_name', 'empresa', 'usuario', 'viaje']


          
        