import django_filters
from contenedor.models import UsuarioContenedor

class UsuarioContenedorFilter(django_filters.FilterSet):   
    contenedor__nombre = django_filters.CharFilter(field_name='contenedor__nombre', lookup_expr='icontains')
    class Meta:
        model = UsuarioContenedor
        fields = {
            'id': ['exact', 'lte'],
            'usuario_id': ['exact'],
            'contenedor__nombre': ['icontains']       
        }