import django_filters
from humano.models.liquidacion_adicional import HumLiquidacionAdicional

class LiquidacionAdicionalFilter(django_filters.FilterSet):
    
    class Meta:
        model = HumLiquidacionAdicional        
        fields = {'id': ['exact'],
                  'liquidacion_id':['exact']}