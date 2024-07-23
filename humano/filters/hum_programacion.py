import django_filters
from humano.models.hum_programacion import HumProgramacion

class HumProgramacionFilter(django_filters.FilterSet):
    class Meta:
        model = HumProgramacion
        fields = {
            'nombre': ['icontains'],
        }