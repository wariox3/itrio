from rest_framework import viewsets, permissions
from humano.models.aporte_detalle import HumAporteDetalle
from humano.serializers.aporte_detalle import HumAporteDetalleSerializador, HumAporteDetalleInformeSerializador
from rest_framework.filters import OrderingFilter
from humano.filters.aporte_detalle import AporteDetalleFilter
from django_filters.rest_framework import DjangoFilterBackend
from utilidades.excel_exportar import ExcelExportar

class HumAporteDetalleViewSet(viewsets.ModelViewSet):
    queryset = HumAporteDetalle.objects.all()
    serializer_class = HumAporteDetalleSerializador
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AporteDetalleFilter
    serializadores = {
        'informe_aporte_detalle': HumAporteDetalleInformeSerializador,
    }   

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return HumAporteDetalleSerializador
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
            titulo = 'Informe aporte detalle'
            nombre_hoja = "aporte_detalles"
            nombre_archivo = "aporte_detalles.xlsx"
            if request.query_params.get('excel_masivo'):
                exporter = ExcelExportar(serializer.data, nombre_hoja, nombre_archivo)
                return exporter.exportar() 
            elif request.query_params.get('excel_informe'): 
                serializador_parametro = self.request.query_params.get('serializador', None)                
                exporter = ExcelExportar(serializer.data, nombre_hoja, nombre_archivo, titulo)
                return exporter.exportar_informe()                    
            else:
                exporter = ExcelExportar(serializer.data, nombre_hoja, nombre_archivo)
                return exporter.exportar_estilo()            
        return super().list(request, *args, **kwargs)