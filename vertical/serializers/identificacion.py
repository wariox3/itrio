from rest_framework import serializers
from vertical.models.identificacion import VerIdentificacion

class VerIdentificacionSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerIdentificacion
        fields = ['id', 'nombre']


class VerIdentificacionSeleccionarSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerIdentificacion
        fields = ['id', 'nombre']        
        