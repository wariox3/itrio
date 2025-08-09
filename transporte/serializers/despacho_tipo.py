from rest_framework import serializers
from transporte.models.despacho_tipo import TteDespachoTipo

class TteDespachoTipoSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteDespachoTipo
        fields = ['id', 'nombre']

class TteDespachoTipoSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteDespachoTipo
        fields = ['id', 'nombre']
