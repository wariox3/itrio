from rest_framework import serializers
from contabilidad.models.conciliacion_detalle import ConConciliacionDetalle

class ConConciliacionDetalleSerializador(serializers.ModelSerializer):     
    documento__numero = serializers.CharField(source='documento.numero', read_only=True)   
    documento__documento_tipo__nombre = serializers.CharField(source='documento.documento_tipo.nombre', read_only=True)   
    cuenta__codigo = serializers.CharField(source='cuenta.codigo', read_only=True)   
    class Meta:
        model = ConConciliacionDetalle
        fields = ['id', 'fecha', 'debito', 'credito', 'detalle', 'estado_conciliado', 
                  'conciliacion', 
                  'cuenta',
                  'cuenta__codigo', 
                  'contacto', 
                  'documento',
                  'documento__numero',
                  'documento__documento_tipo__nombre']  
        select_related_fields = ['conciliacion', 'cuenta', 'contacto', 'documento']              
        