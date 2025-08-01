import django_filters
from ruteo.models.novedad import RutNovedad

class NovedadFilter(django_filters.FilterSet):    
    class Meta:
        model = RutNovedad
        fields = {'id': ['exact'],
                  'estado_solucion': ['exact'], 
                  'nuevo_complemento': ['exact'],
                  'visita_id': ['exact'],
                  }