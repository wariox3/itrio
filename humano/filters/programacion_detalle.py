import django_filters
from humano.models.programacion_detalle import HumProgramacionDetalle

class ProgramacionDetalleFilter(django_filters.FilterSet):
    
    class Meta:
        model = HumProgramacionDetalle        
        fields = {'id': ['exact', 'lte'],
                  'programacion_id':['exact']}