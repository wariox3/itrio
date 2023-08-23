from rest_framework import serializers
from general.models.documento_tipo import DocumentoTipo

class DocumentoTipoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DocumentoTipo
        fields = ['id', 'nombre'] 
        