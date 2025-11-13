import django_filters
from vertical.models.verificacion import VerVerificacion
class VerVerificacionFilter(django_filters.FilterSet):    

    class Meta:
        model = VerVerificacion
        fields = {  
                    'id': ['exact'],
                    'estado_proceso': ['exact'],
                    'verificado': ['exact']
                }