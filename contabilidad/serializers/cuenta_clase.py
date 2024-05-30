from rest_framework import serializers
from contabilidad.models.cuenta_clase import CuentaClase

class CuentaClaseSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = CuentaClase
        fields = ['id']
        