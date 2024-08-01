from general.models.configuracion import GenConfiguracion
from general.models.empresa import Empresa

from rest_framework import serializers
from decouple import config

class GenConfiguracionSerializador(serializers.HyperlinkedModelSerializer):
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())
    class Meta:
        model = GenConfiguracion
        fields = [
            'id',
            'empresa',
            'formato_factura',
            'informacion_factura',
            'informacion_factura_superior',
            'venta_asesor',
            'venta_sede'
        ]      
        
class GenConfiguracionActualizarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenConfiguracion
        fields = [
            'formato_factura', 
            'informacion_factura', 
            'informacion_factura_superior',
            'venta_asesor',
            'venta_sede'
        ]