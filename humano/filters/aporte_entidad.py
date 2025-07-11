import django_filters
from humano.models.aporte_entidad import HumAporteEntidad

class AporteEntidadFilter(django_filters.FilterSet):
 
    class Meta:
        model = HumAporteEntidad        
        fields = {'id': ['exact', 'lte'],
                  'aporte_id':['exact']}