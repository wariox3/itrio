from general.models.configuracion import Configuracion
from general.models.empresa import Empresa

from rest_framework import serializers
from decouple import config

class ConfiguracionSerializador(serializers.HyperlinkedModelSerializer):
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())
    class Meta:
        model = Configuracion
        fields = [
            'id',
            'empresa',
            'formato_factura']      