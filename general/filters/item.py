import django_filters
from general.models.item import GenItem

class ItemFilter(django_filters.FilterSet):    
    class Meta:
        model = GenItem        
        fields = {'id': ['exact'],
                  'nombre': ['exact','icontains'],
                  'codigo': ['exact','icontains'],
                  'inventario': ['exact']}