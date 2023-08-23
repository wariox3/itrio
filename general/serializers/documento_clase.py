from rest_framework import serializers
from general.models.documento_clase import DocumentoClase

class DocumentoClaseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DocumentoClase
        fields = ['id', 'nombre'] 
        