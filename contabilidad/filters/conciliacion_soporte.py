import django_filters
from contabilidad.models.conciliacion_soporte import ConConciliacionSoporte

class ConciliacionSoporteFilter(django_filters.FilterSet):    
    class Meta:
        model = ConConciliacionSoporte
        fields = {'id': ['exact'],
                  'conciliacion_id': ['exact']}