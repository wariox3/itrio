import django_filters
from contenedor.models import User

class UsuarioFilter(django_filters.FilterSet):    
    
    class Meta:
        model = User
        fields = {
            'id': ['exact'],
        }