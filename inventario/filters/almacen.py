import django_filters
from inventario.models.almacen import InvAlmacen

class AlmacenFilter(django_filters.FilterSet):    
    class Meta:
        model = InvAlmacen        
        fields = {'id': ['exact'],
                  'nombre': ['exact','icontains']}