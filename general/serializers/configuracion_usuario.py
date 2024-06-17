from general.models.configuracion_usuario import ConfiguracionUsuario
from general.models.empresa import Empresa
from general.models.sede import Sede

from rest_framework import serializers
from decouple import config

class ConfiguracionUsuarioSerializador(serializers.HyperlinkedModelSerializer):
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())
    class Meta:
        model = ConfiguracionUsuario
        fields = [
            'id',
            'empresa',
            'usuario'
        ] 

class ConfiguracionUsuarioActualizarSerializador(serializers.HyperlinkedModelSerializer):
    sede = serializers.PrimaryKeyRelatedField(queryset=Sede.objects.all(), default=None, allow_null=True)
    class Meta:
        model = ConfiguracionUsuario
        fields = [
            'sede'
        ]             