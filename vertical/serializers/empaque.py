from rest_framework import serializers
from vertical.models.empaque import VerEmpaque

class VerEmpaqueSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerEmpaque
        fields = ['id', 'nombre', 'codigo']

class VerEmpaqueSeleccionarSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerEmpaque
        fields = ['id', 'nombre', 'codigo']        
        