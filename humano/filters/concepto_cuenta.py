import django_filters
from humano.models.concepto_cuenta import HumConceptoCuenta

class ConceptoCuentaFilter(django_filters.FilterSet):
    class Meta:
        model = HumConceptoCuenta        
        fields = {
            'concepto': ['exact'],
        }