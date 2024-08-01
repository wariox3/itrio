import django_filters
from humano.models.programacion import HumProgramacion

class HumProgramacionFilter(django_filters.FilterSet):
    class Meta:
        model = HumProgramacion
        fields = {
            'nombre': ['icontains'],
        }