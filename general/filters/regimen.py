import django_filters
from general.models.regimen import GenRegimen

class RegimenFilter(django_filters.FilterSet):    
    class Meta:
        model = GenRegimen        
        fields = {
            'id': ['exact', 'lte'],
            'nombre':['icontains']
        }