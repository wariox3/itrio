import django_filters
from vertical.models.precio_detalle import VerPrecioDetalle
class VerPrecioDetalleFilter(django_filters.FilterSet):    

    class Meta:
        model = VerPrecioDetalle
        fields = {  
                    'id': ['exact'],
                }