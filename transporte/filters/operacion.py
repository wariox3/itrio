import django_filters
from transporte.models.operacion import TteOperacion

class OperacionFilter(django_filters.FilterSet):    
    ciudad__nombre = django_filters.CharFilter(field_name='ciudad__nombre', lookup_expr='icontains')
    class Meta:
        model = TteOperacion
        fields = {'id': ['exact'],
                  'ciudad__nombre': ['exact', 'icontains'],    
                  'ciudad_id': ['exact'],                   
                  'nombre': ['exact', 'icontains'],              
                  }
        