import django_filters
from general.models.precio import GenPrecio

class PrecioFilter(django_filters.FilterSet):    
    class Meta:
        model = GenPrecio        
        fields = {'id': ['exact'],
                  'nombre': ['exact','icontains']}