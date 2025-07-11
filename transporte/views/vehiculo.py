from rest_framework import viewsets, permissions
from transporte.models.vehiculo import TteVehiculo
from transporte.serializers.vehiculo import TteVehiculoSerializador
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from utilidades.excel_exportar import ExcelExportar


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = TteVehiculo.objects.all()
    serializer_class = TteVehiculoSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter] 

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return TteVehiculoSerializador
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
            exporter = ExcelExportar(serializer.data, nombre_hoja="vehículos", nombre_archivo="vehículos.xlsx", titulo="Vehículos")
            return exporter.exportar()
        return super().list(request, *args, **kwargs)   