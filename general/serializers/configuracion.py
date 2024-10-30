from general.models.configuracion import GenConfiguracion
from general.models.empresa import GenEmpresa

from rest_framework import serializers
from decouple import config

class GenConfiguracionSerializador(serializers.HyperlinkedModelSerializer):
    empresa = serializers.PrimaryKeyRelatedField(queryset=GenEmpresa.objects.all())
    class Meta:
        model = GenConfiguracion
        fields = ['id', 'empresa', 'informacion_factura', 'informacion_factura_superior',
            'venta_asesor', 'venta_sede', 
            'gen_uvt',
            'hum_factor', 'hum_salario_minimo', 'hum_auxilio_transporte'
        ]      
        
class GenConfiguracionActualizarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenConfiguracion
        fields = ['informacion_factura', 'informacion_factura_superior', 'venta_asesor',
            'venta_sede', 
            'gen_uvt',
            'hum_factor', 'hum_salario_minimo', 'hum_auxilio_transporte'
        ]