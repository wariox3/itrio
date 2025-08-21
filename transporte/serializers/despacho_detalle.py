from rest_framework import serializers
from transporte.models.despacho_detalle import TteDespachoDetalle

class TteDespachoDetalleSerializador(serializers.ModelSerializer):   
    guia__ciudad_destino__nombre = serializers.CharField(source='guia.ciudad_destino.nombre', read_only=True, allow_null=True, default=None)
    guia__destinatario__nombre_corto = serializers.CharField(source='guia.destinatario.nombre_corto', read_only=True, allow_null=True, default=None)
    class Meta:
        model = TteDespachoDetalle
        fields = ['id', 'fecha_registro', 'unidades', 'peso', 'volumen', 'peso_facturado', 'costo', 'declara', 
                  'flete', 'manejo', 'recaudo', 'cobro_entrega', 'despacho', 'guia', 'guia__ciudad_destino__nombre', 'guia__destinatario__nombre_corto'] 
        select_related_fields = ['guia']      
 