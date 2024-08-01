from rest_framework import serializers
from general.models.documento_clase import GenDocumentoClase

class GenDocumentoClaseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GenDocumentoClase
        fields = ['id', 'nombre'] 
        