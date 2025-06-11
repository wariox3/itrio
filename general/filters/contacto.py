import django_filters
from general.models.contacto import GenContacto

class ContactoFilter(django_filters.FilterSet):    
    class Meta:
        model = GenContacto        
        fields = {'id': ['exact', 'lte'],
                  'numero_identificacion': ['exact', 'icontains'],
                  'nombre_corto': ['exact','icontains'], 
                  'cliente': ['exact'], 
                  'proveedor': ['exact'], 
                  'empleado': ['exact']}