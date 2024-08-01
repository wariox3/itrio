from general.models.configuracion import Configuracion
from general.models.empresa import Empresa

from rest_framework import serializers
from decouple import config

class GenConfiguracionSerializador(serializers.HyperlinkedModelSerializer):
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())
    class Meta:
        model = Configuracion
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
        model = Configuracion
        fields = [
            'formato_factura', 
            'informacion_factura', 
            'informacion_factura_superior',
            'venta_asesor',
            'venta_sede'
        ]