import django_filters
from humano.models.programacion import HumProgramacion

class Programacionilter(django_filters.FilterSet):
    class Meta:
        model = HumProgramacion        
        fields = {'id': ['exact', 'lte']}