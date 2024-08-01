from rest_framework import serializers
from contabilidad.models.con_cuenta_clase import ConCuentaClase

class CuentaClaseSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConCuentaClase
        fields = ['id']
        