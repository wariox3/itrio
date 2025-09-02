from general.models.documento_guia import GenDocumentoGuia
from rest_framework import serializers

class GenDocumentoGuiaSerializador(serializers.ModelSerializer):
    class Meta:
        model = GenDocumentoGuia
        fields = ['id', 'unidades', 'peso', 'volumen', 'peso_facturado', 'costo', 'declara', 'flete', 'manejo', 'recaudo', 'cobro_entrega', 
                  'documento', 
                  'guia']   
        select_related_fields = ['guia', 'documento']     
  

        