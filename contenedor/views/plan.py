from rest_framework import viewsets, permissions
from contenedor.models import CtnPlan
from contenedor.serializers.plan import CtnPlanSerializador, CtnPlanListaSerializador
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from contenedor.filters.plan import PlanFilter

class PlanViewSet(viewsets.ModelViewSet):
    queryset = CtnPlan.objects.all()
    serializer_class = CtnPlanSerializador    
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PlanFilter 
    serializadores = {'lista': CtnPlanListaSerializador}

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return CtnPlanSerializador
        return self.serializadores[serializador_parametro]

    def get_queryset(self):
        queryset = super().get_queryset()
        serializer_class = self.get_serializer_class()        
        select_related = getattr(serializer_class.Meta, 'select_related_fields', [])
        if select_related:
            queryset = queryset.select_related(*select_related)        
        campos = serializer_class.Meta.fields        
        if campos and campos != '__all__':
            queryset = queryset.only(*campos) 
        return queryset 
    
    def list(self, request, *args, **kwargs):
        if request.query_params.get('excel'):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
        return super().list(request, *args, **kwargs)