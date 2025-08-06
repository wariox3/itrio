import django_filters
from transporte.models.negocio import TteNegocio

class NegocioFilter(django_filters.FilterSet):    
    
    class Meta:
        model = TteNegocio
        fields = {'id': ['exact']                  
                  }