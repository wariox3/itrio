from rest_framework import viewsets, permissions
from transporte.models.conductor import TteConductor
from transporte.serializers.conductor import TteConductorSerializador
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from utilidades.excel_exportar import ExcelExportar


class ConductorViewSet(viewsets.ModelViewSet):
    queryset = TteConductor.objects.all()
    serializer_class = TteConductorSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter] 

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return TteConductorSerializador
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
            exporter = ExcelExportar(serializer.data, nombre_hoja="conductores", nombre_archivo="conductores.xlsx", titulo="Conductores")
            return exporter.exportar()
        return super().list(request, *args, **kwargs)   