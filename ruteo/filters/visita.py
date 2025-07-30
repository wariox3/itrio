import django_filters
from ruteo.models.visita import RutVisita

class VisitaFilter(django_filters.FilterSet):    
    class Meta:
        model = RutVisita
        fields = {'id': ['exact'],
                  'despacho_id' : ['exact'],
                  'estado_entregado': ['exact']}