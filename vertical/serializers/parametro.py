from rest_framework import serializers
from vertical.models.parametro import VerParametro

class VerParametroSerializador(serializers.ModelSerializer):
   
    class Meta:
        model = VerParametro
        fields = ['id', 'version_ruteo'] 
