import django_filters
from transporte.models.despacho import TteDespacho

class DespachoFilter(django_filters.FilterSet):    
    
    class Meta:
        model = TteDespacho
        fields = {'id': ['exact']                  
                  }