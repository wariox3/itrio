from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from general.models.sede import GenSede
from general.serializers.sede import GenSedeSerializador, GenSedeListaSerializador
from general.filters.sede import SedeFilter

class SedeViewSet(viewsets.ModelViewSet):
    queryset = GenSede.objects.all()
    serializer_class = GenSedeSerializador    
    permission_classes = [permissions.IsAuthenticated]               

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SedeFilter 
    queryset = GenSede.objects.all()   
    serializadores = {'lista': GenSedeListaSerializador}

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return GenSedeSerializador
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
            exporter = ExportarExcel(serializer.data, sheet_name="sedes", filename="sedes.xlsx")
            return exporter.export()
        return super().list(request, *args, **kwargs)    