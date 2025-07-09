import django_filters
from general.models.resolucion import GenResolucion

class ResolucionFilter(django_filters.FilterSet):    
    class Meta:
        model = GenResolucion        
        fields = {'id': ['exact'],
                  'numero': ['exact','icontains'],
                  'venta': ['exact'],
                  'compra': ['exact'],}