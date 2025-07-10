import django_filters
from humano.models.aporte import HumAporte

class AporteFilter(django_filters.FilterSet):
    
    class Meta:
        model = HumAporte        
        fields = {'id': ['exact', 'lte'],
                  'fecha_desde': ['gte', 'lte', 'gt', 'lt', 'exact'],
                  'fecha_hasta': ['gte', 'lte', 'gt', 'lt', 'exact'],
                  'mes': ['exact'],
                  'anio': ['exact'],}