from rest_framework import serializers
from transporte.models.guia import TteGuia


class TteGuiaSerializador(serializers.ModelSerializer):   

    class Meta:
        model = TteGuia
        fields = ['id', 'fecha', 'destinatario', 'ciudad_destino', 'ciudad_origen', 'cliente', 'contacto', 'empaque',
                  'servicio', 'producto', 'ruta', 'zona', 'operacion_cargo', 'operacion_ingreso', 'unidades', 'peso',
                  'volumen', 'peso_facturado', 'declara', 'flete', 'manejo', 'recaudo', 'cobro_entrega', 'contenido_verificado',
                  'mercancia_peligrosa', 'requiere_cita', 'comentario']
        select_related_fields = ['contacto', 'destinatario', 'ciudad_destino', 'ciudad_origen', 'cliente', 'empaque'
                                 'servicio', 'producto', 'ruta', 'zona', 'operacion_cargo', 'operacion_ingreso']  
    
