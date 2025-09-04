from general.models.documento_guia import GenDocumentoGuia
from rest_framework import serializers

class GenDocumentoGuiaSerializador(serializers.ModelSerializer):
    guia__fecha = serializers.DateField(source='guia.fecha', read_only=True, allow_null=True, default=None)
    guia__ciudad_destino__nombre = serializers.CharField(source='guia.ciudad_destino.nombre', read_only=True, allow_null=True, default=None)
    guia__cliente__nombre_corto = serializers.CharField(source='guia.cliente.nombre_corto', read_only=True, allow_null=True, default=None)
    guia__estado_entregado = serializers.CharField(source='guia.estado_entregado', read_only=True, allow_null=True, default=None)
    class Meta:
        model = GenDocumentoGuia
        fields = ['id', 'unidades', 'peso', 'volumen', 'peso_facturado', 'costo', 'declara', 'flete', 'manejo', 'recaudo', 'cobro_entrega', 
                  'documento', 'guia', 'guia__fecha', 'guia__ciudad_destino__nombre', 'guia__cliente__nombre_corto', 'guia__estado_entregado']   
        select_related_fields = ['guia', 'documento']     
  

        