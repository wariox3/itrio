from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from general.models.asesor import GenAsesor
from general.serializers.asesor import GenAsesorSerializador
from utilidades.excel_exportar import ExcelExportar
from general.filters.asesor import AsesorFilter
from rest_framework.response import Response

class AsesorViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AsesorFilter 
    queryset = GenAsesor.objects.all()   
    serializadores = {'lista': GenAsesorSerializador}

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return GenAsesorSerializador
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
            exporter = ExcelExportar(serializer.data, nombre_hoja="asesores", nombre_archivo="asesores.xlsx", titulo="Asesores")
            return exporter.exportar()
        return super().list(request, *args, **kwargs)   

    @action(detail=False, methods=["get"], url_path=r'seleccionar')
    def seleccionar_action(self, request):
        limit = request.query_params.get('limit', 10)
        nombre_corto = request.query_params.get('nombre_corto_icontains', None)
        queryset = self.get_queryset()
        if nombre_corto:
            queryset = queryset.filter(nombre_corto__icontains=nombre_corto)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = self.get_serializer(queryset, many=True)        
        return Response(serializer.data)