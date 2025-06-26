from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from humano.models.cargo import HumCargo
from humano.serializers.cargo import HumCargoSerializador, HumCargoListaSerializador
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
            exporter = ExcelExportar(serializer.data, sheet_name="cargos", filename="cargos.xlsx")
            return exporter.exportar()
        return super().list(request, *args, **kwargs)   