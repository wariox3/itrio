from general.models.error_importar import GenErrorImportar
from general.models.documento import GenDocumento
from rest_framework import serializers

class GenErrorImportarSerializador(serializers.HyperlinkedModelSerializer):
    documento = serializers.PrimaryKeyRelatedField(queryset=GenDocumento.objects.all())
    class Meta:
        model = GenErrorImportar
        fields = ['id', 'fila', 'mensaje', 'documento']
  