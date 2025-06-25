from rest_framework import viewsets, permissions
from general.models.precio import GenPrecio
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from general.serializers.precio import GenPrecioSerializador, GenPrecioListaSerializador
from general.filters.precio import PrecioFilter
from utilidades.excel_exportar import ExcelExportar

class PrecioViewSet(viewsets.ModelViewSet):
    queryset = GenPrecio.objects.all()
    serializer_class = GenPrecioSerializador
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PrecioFilter 
    permission_classes = [permissions.IsAuthenticated]
    serializadores = {'lista': GenPrecioListaSerializador}

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return GenPrecioSerializador
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
            exporter = ExcelExportar(serializer.data, sheet_name="precios", filename="precios.xlsx")
            return exporter.export()
        return super().list(request, *args, **kwargs)    