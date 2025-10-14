import django_filters
from general.models.precio_detalle import GenPrecioDetalle

class PrecioDetalleFilter(django_filters.FilterSet):    
    class Meta:
        model = GenPrecioDetalle        
        fields = {'id': ['exact'],
                  'precio_id': ['exact']}