from general.models.documento_guia import GenDocumentoGuia
from rest_framework import serializers

class GenDocumentoGuiaSerializador(serializers.ModelSerializer):
    class Meta:
        model = GenDocumentoGuia
        fields = ['id', 'flete', 'manejo']   
        select_related_fields = ['guia']     
  

        