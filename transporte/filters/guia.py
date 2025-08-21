import django_filters
from transporte.models.guia import TteGuia

class GuiaFilter(django_filters.FilterSet):    
    
    class Meta:
        model = TteGuia
        fields = {'id': ['exact'],
                  'estado_despachado': ['exact']                  
                  }