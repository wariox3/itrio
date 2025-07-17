from rest_framework import serializers
from transporte.models.empaque import TteEmpaque

class TteEmpaqueSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteEmpaque
        fields = ['id', 'nombre']

class TteEmpaqueSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteEmpaque
        fields = ['id', 'nombre']
