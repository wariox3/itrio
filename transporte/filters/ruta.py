import django_filters
from transporte.models.ruta import TteRuta

class RutaFilter(django_filters.FilterSet):    
    
    class Meta:
        model = TteRuta
        fields = {'id': ['exact'],
                'nombre': ['exact', 'icontains'],                        
                  }