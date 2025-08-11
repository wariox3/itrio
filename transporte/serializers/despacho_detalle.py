from rest_framework import serializers
from transporte.models.despacho_detalle import TteDespachoDetalle

class TteDespachoDetalleSerializador(serializers.ModelSerializer):   

    class Meta:
        model = TteDespachoDetalle
        fields = ['id', 'fecha_registro', 'unidades', 'peso', 'volumen', 'peso_facturado', 'costo', 'declara', 
                  'flete', 'manejo', 'recaudo', 'cobro_entrega', 'despacho', 'guia'] 
    
 