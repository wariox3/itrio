import django_filters
from contabilidad.models.periodo import ConPeriodo

class PeriodoFilter(django_filters.FilterSet):    
    class Meta:
        model = ConPeriodo
        fields = {'id': ['exact']}