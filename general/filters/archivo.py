import django_filters
from general.models.archivo import GenArchivo

class ArchivoFilter(django_filters.FilterSet):    
    class Meta:
        model = GenArchivo        
        fields = {
            'id': ['exact', 'lte'],
            'documento_id':['exact',],
            'modelo':['exact',]
        }