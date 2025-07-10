import django_filters
from humano.models.aporte_detalle import HumAporteDetalle

class AporteDetalleFilter(django_filters.FilterSet):
    aporte_contrato__contrato__contacto__nombre_corto = django_filters.CharFilter(field_name='aporte_contrato__contrato__contacto__nombre_corto', lookup_expr='icontains')
    aporte_contrato__contrato_id =  django_filters.NumberFilter(field_name='aporte_contrato__contrato_id', lookup_expr='exact')
 
    class Meta:
        model = HumAporteDetalle        
        fields = {'id': ['exact', 'lte'],
                  'aporte_contrato__aporte_id':['exact'],
                  'aporte_contrato__contrato__contacto__nombre_corto':['icontains'],
                  'aporte_contrato__contrato_id':['exact'],
                  'aporte_contrato_id':['exact'],}