from rest_framework import viewsets, permissions, status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.conciliacion import ConConciliacion
from contabilidad.serializers.conciliacion import ConConciliacionSerializador
from contabilidad.filters.conciliacion import ConciliacionFilter
from utilidades.excel_exportar import ExcelExportar


class ConciliacionViewSet(viewsets.ModelViewSet):
    queryset = ConConciliacion.objects.all()
    serializer_class = ConConciliacionSerializador
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ConciliacionFilter 
    permission_classes = [permissions.IsAuthenticated]
    serializadores = {'lista': ConConciliacionSerializador}

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return ConConciliacionSerializador
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
            exporter = ExcelExportar(serializer.data, nombre_hoja="conciliaciones", nombre_archivo="conciliaciones.xlsx", titulo="Conciliaciones")            
            return exporter.exportar()
        return super().list(request, *args, **kwargs)    
           
        
    