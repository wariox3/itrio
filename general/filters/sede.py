import django_filters
from general.models.sede import GenSede

class SedeFilter(django_filters.FilterSet):    
    class Meta:
        model = GenSede        
        fields = {'id': ['exact'],
                  'nombre': ['exact','icontains']}