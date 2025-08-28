import django_filters
from transporte.models.despacho_detalle import TteDespachoDetalle

class DespachoDetalleFilter(django_filters.FilterSet):    
    
    class Meta:
        model = TteDespachoDetalle
        fields = {'id': ['exact'],
                  'despacho_id': ['exact'],
                  'guia_id': ['exact'],
                  }