import django_filters
from contenedor.models import UsuarioContenedor

class UsuarioContenedorFilter(django_filters.FilterSet):   
    contenedor__nombre = django_filters.CharFilter(field_name='contenedor__nombre', lookup_expr='icontains')
    contenedor__reddoc = django_filters.BooleanFilter(field_name='contenedor__reddoc', lookup_expr='exact')    
    contenedor__ruteo = django_filters.BooleanFilter(field_name='contenedor__ruteo', lookup_expr='exact')    
    class Meta:
        model = UsuarioContenedor
        fields = {
            'id': ['exact', 'lte'],
            'contenedor_id': ['exact'],
            'usuario_id': ['exact'],
            'rol': ['exact'],
            'contenedor__nombre': ['icontains'],    
            'contenedor__reddoc': ['exact'],
            'contenedor__ruteo': ['exact'],
        }