import django_filters
from ruteo.models.visita import RutVisita

class VisitaFilter(django_filters.FilterSet):    
    class Meta:
        model = RutVisita
        fields = {'id': ['exact'],
                  'despacho_id' : ['exact'],
                  'numero': ['exact'],
                  'documento': ['exact', 'icontains'],
                  'estado_entregado': ['exact'],
                  'estado_despacho': ['exact'],
                  'estado_decodificado': ['exact'],
                  'estado_decodificado_alerta': ['exact'],
                  'fecha': ['gte', 'lte', 'gt', 'lt', 'exact'], 
                  'fecha_entrega': ['gte', 'lte', 'gt', 'lt', 'exact'], 
                  'destinatario':['icontains'],
                  }