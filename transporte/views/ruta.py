from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from transporte.models.ruta import TteRuta
from transporte.serializers.ruta import TteRutaSerializador, TteRutaSeleccionarSerializador
from transporte.filters.ruta import RutaFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class RutaViewSet(viewsets.ModelViewSet):
    queryset = TteRuta.objects.all()
    serializer_class = TteRutaSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RutaFilter 
    serializadores = {
        'lista': TteRutaSerializador,
    } 

    @action(detail=False, methods=["get"], url_path=r'seleccionar')
    def seleccionar_action(self, request):
        limit = request.query_params.get('limit', 10)
        nombre = request.query_params.get('nombre__icontains', None)
        queryset = self.get_queryset()
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = TteRutaSeleccionarSerializador(queryset, many=True)        
        return Response(serializer.data)        
    
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
        if request.query_params.get('lista_completa', '').lower() == 'true':
            self.pagination_class = None
        return super().list(request, *args, **kwargs)