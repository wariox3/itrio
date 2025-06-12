import django_filters
from general.models.documento_tipo import GenDocumentoTipo
from django_filters import NumberFilter

class DocumentoTipoFilter(django_filters.FilterSet):
    class Meta:
        model = GenDocumentoTipo        
        fields = {'venta': ['exact'], 
                  'operacion': ['exact'],
                  'pos': ['exact']}