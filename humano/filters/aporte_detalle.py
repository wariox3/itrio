import django_filters
from humano.models.aporte_detalle import HumAporteDetalle

class AporteDetalleFilter(django_filters.FilterSet):
    
    class Meta:
        model = HumAporteDetalle        
        fields = {'id': ['exact', 'lte'],
                  'aporte_id':['exact'],
                  'aporte_contrato_id':['exact']}