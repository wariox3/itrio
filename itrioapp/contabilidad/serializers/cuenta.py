from rest_framework import serializers
from contabilidad.models.cuenta import Cuenta

class CuentaSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Cuenta
        fields = ['id']
        