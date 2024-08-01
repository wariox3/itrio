from general.models.configuracion_usuario import GenConfiguracionUsuario
from general.models.empresa import GenEmpresa
from general.models.sede import GenSede

from rest_framework import serializers
from decouple import config

class GenConfiguracionUsuarioSerializador(serializers.HyperlinkedModelSerializer):
    empresa = serializers.PrimaryKeyRelatedField(queryset=GenEmpresa.objects.all())
    class Meta:
        model = GenConfiguracionUsuario
        fields = [
            'id',
            'empresa',
            'usuario'
        ] 

class GenConfiguracionUsuarioActualizarSerializador(serializers.HyperlinkedModelSerializer):
    sede = serializers.PrimaryKeyRelatedField(queryset=GenSede.objects.all(), default=None, allow_null=True)
    class Meta:
        model = GenConfiguracionUsuario
        fields = [
            'sede'
        ]             