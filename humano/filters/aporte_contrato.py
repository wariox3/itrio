import django_filters
from humano.models.aporte_contrato import HumAporteContrato

class AporteContratoFilter(django_filters.FilterSet):
    contrato__contacto__nombre_corto = django_filters.CharFilter(field_name='contrato__contacto__nombre_corto', lookup_expr='icontains')
    contrato__contacto_id =  django_filters.NumberFilter(field_name='contrato_contacto_id', lookup_expr='exact')
    class Meta:
        model = HumAporteContrato        
        fields = {'id': ['exact', 'lte'],
                  'aporte_id':['exact'],
                  'contrato__contacto__nombre_corto':['icontains'],
                  'contrato__contacto_id':['exact'],}