import django_filters
from general.models.documento_guia import GenDocumentoGuia

class DocumentoGuiaFilter(django_filters.FilterSet):
    
    class Meta:
        model = GenDocumentoGuia        
        fields = {
                    'id': ['exact', 'lte'],
                }