import django_filters
from contabilidad.models.conciliacion import ConConciliacion

class ConciliacionFilter(django_filters.FilterSet):    
    class Meta:
        model = ConConciliacion
        fields = {'id': ['exact']}