from rest_framework import viewsets, permissions
from humano.models.aporte_contrato import HumAporteContrato
from humano.serializers.aporte_contrato import HumAporteContratoSerializador, HumAporteContratoInformeSerializador
from rest_framework.filters import OrderingFilter
from humano.filters.aporte_contrato import AporteContratoFilter
from django_filters.rest_framework import DjangoFilterBackend
from utilidades.excel_exportar import ExcelExportar

class HumAporteContratoViewSet(viewsets.ModelViewSet):
    queryset = HumAporteContrato.objects.all()
    serializer_class = HumAporteContratoSerializador
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AporteContratoFilter   
    serializadores = {
        'informe_aporte_contrato': HumAporteContratoInformeSerializador,
    }

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return HumAporteContratoSerializador
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
            titulo = 'Informe aporte contrato'
            nombre_hoja = "aporte_contratos"
            nombre_archivo = "aporte_contratos.xlsx"
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
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()                        
        aporte = instance.aporte
        response = super().destroy(request, *args, **kwargs)
        aporte.contratos -= 1
        aporte.empleados -= 1
        aporte.save()
        return response
            
 