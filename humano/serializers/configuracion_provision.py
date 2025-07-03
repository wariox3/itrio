from rest_framework import serializers
from humano.models.configuracion_provision import HumConfiguracionProvision
from humano.models.tipo_costo import HumTipoCosto
from contabilidad.models.cuenta import ConCuenta

class HumConfiguracionProvisionSerializador(serializers.ModelSerializer):
    tipo_costo__nombre = serializers.CharField(source='tipo_costo.nombre', read_only=True)
    cuenta_debito__nombre = serializers.CharField(source='cuenta_debito.nombre', read_only=True)
    cuenta_debito__codigo = serializers.CharField(source='cuenta_debito.codigo', read_only=True)
    cuenta_credito__nombre = serializers.CharField(source='cuenta_credito.nombre', read_only=True)
    cuenta_credito__codigo = serializers.CharField(source='cuenta_credito.codigo', read_only=True)
    class Meta:
        model = HumConfiguracionProvision
        fields = ['id', 'tipo', 'tipo_costo', 'tipo_costo__nombre' , 'cuenta_debito' ,'cuenta_debito__nombre', 'cuenta_debito__codigo', 'cuenta_credito', 'cuenta_credito__nombre', 'cuenta_credito__codigo']  
        select_related_fields = ['tipo_costo', 'cuenta_debito', 'cuenta_credito']        

          