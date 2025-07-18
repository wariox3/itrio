from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from humano.models.cargo import HumCargo
from humano.serializers.cargo import HumCargoSerializador, HumCargoListaSerializador, HumCargoSeleccionarSerializador
from utilidades.excel_exportar import ExcelExportar
from humano.filters.cargo import CargoFilter

class HumCargoViewSet(viewsets.ModelViewSet):
    queryset = HumCargo.objects.all()
    serializer_class = HumCargoSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CargoFilter 
    permission_classes = [permissions.IsAuthenticated]
    serializadores = {'lista': HumCargoListaSerializador}   

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return HumCargoSerializador
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
            exporter = ExcelExportar(serializer.data, nombre_hoja="cargos", nombre_archivo="cargos.xlsx", titulo="Cargos")            
            return exporter.exportar()
        return super().list(request, *args, **kwargs)   
    
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
        serializer = HumCargoSeleccionarSerializador(queryset, many=True)        
        return Response(serializer.data)      