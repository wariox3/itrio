import django_filters
from contabilidad.models.cuenta_grupo import ConCuentaGrupo

class CuentaGrupoFilter(django_filters.FilterSet):    
    class Meta:
        model = ConCuentaGrupo
        fields = {'id': ['exact', 'gte', 'lte'],
                  'nombre': ['exact','icontains']}