from general.models.configuracion import GenConfiguracion
from general.models.empresa import GenEmpresa
from general.models.documento_tipo import GenDocumentoTipo
from humano.models.entidad import HumEntidad

from rest_framework import serializers
from decouple import config

class GenConfiguracionSerializador(serializers.HyperlinkedModelSerializer):
    empresa = serializers.PrimaryKeyRelatedField(queryset=GenEmpresa.objects.all())
    hum_entidad_riesgo = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all(), default=None, allow_null=True)
    pos_documento_tipo = serializers.PrimaryKeyRelatedField(queryset=GenDocumentoTipo.objects.all(), default=None, allow_null=True)
    class Meta:
        model = GenConfiguracion
        fields = ['id', 'empresa', 'informacion_factura', 'informacion_factura_superior', 
            'gen_uvt',
            'hum_factor', 'hum_salario_minimo', 'hum_auxilio_transporte', 'hum_entidad_riesgo',
            'pos_documento_tipo'
        ]      
        
class GenConfiguracionActualizarSerializador(serializers.HyperlinkedModelSerializer):
    hum_entidad_riesgo = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all(), default=None, allow_null=True)
    pos_documento_tipo = serializers.PrimaryKeyRelatedField(queryset=GenDocumentoTipo.objects.all(), default=None, allow_null=True)
    class Meta:
        model = GenConfiguracion
        fields = ['informacion_factura', 'informacion_factura_superior',
            'gen_uvt',
            'hum_factor', 'hum_salario_minimo', 'hum_auxilio_transporte', 'hum_entidad_riesgo',
            'pos_documento_tipo'
        ]