import django_filters
from humano.models.aporte_contrato import HumAporteContrato

class AporteContratoFilter(django_filters.FilterSet):
    
    class Meta:
        model = HumAporteContrato        
        fields = {'id': ['exact', 'lte'],
                  'aporte_id':['exact']}