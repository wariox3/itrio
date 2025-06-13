import django_filters
from ruteo.models.despacho import RutDespacho

class DespachoFilter(django_filters.FilterSet):    
    class Meta:
        model = RutDespacho
        fields = {'id': ['exact'],
                  'nombre': ['exact','icontains']}