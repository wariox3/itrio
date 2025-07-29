import django_filters
from ruteo.models.despacho import RutDespacho

class DespachoFilter(django_filters.FilterSet):    
    class Meta:
        model = RutDespacho
        fields = {'id': ['exact'],
                  'estado_aprobado': ['exact'], 
                  'estado_anulado': ['exact'],
                  'estado_terminado': ['exact'], }