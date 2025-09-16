import django_filters
from vertical.models.conductor import VerConductor
class VerConductorFilter(django_filters.FilterSet):    

    class Meta:
        model = VerConductor
        fields = {  
                    'id': ['exact'],
                    'usuario_id': ['exact']
                }