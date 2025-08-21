import django_filters
from contenedor.models import UsuarioContenedor

class UsuarioContenedorFilter(django_filters.FilterSet):   
    
     
    class Meta:
        model = UsuarioContenedor
        fields = {
            'id': ['exact', 'lte'],
            'usuario_id': ['exact']        
        }