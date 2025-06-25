import django_filters
from general.models.banco import GenBanco

class BancoFilter(django_filters.FilterSet):    
    class Meta:
        model = GenBanco        
        fields = {
            'id': ['exact', 'lte'],
            'nombre':['icontains']
        }