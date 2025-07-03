from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from general.models.documento_detalle import GenDocumentoDetalle
from general.serializers.documento_detalle import GenDocumentoDetalleSerializador, GenDocumentoDetalleInformeVentaSerializador, GenDocumentoDetalleAgregarDocumentoSerializador
from general.filters.documento_detalle import DocumentoDetalleFilter
from utilidades.excel_exportar import ExcelExportar
from rest_framework.decorators import action

class DocumentoDetalleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter] 
    filterset_class = DocumentoDetalleFilter
    queryset = GenDocumentoDetalle.objects.all()
    serializadores = {
        'informe_venta': GenDocumentoDetalleInformeVentaSerializador,
        'agregar_documento':  GenDocumentoDetalleAgregarDocumentoSerializador
    }
    
    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return GenDocumentoDetalleSerializador
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
            titulo = 'Informe documentos detalles'
            nombre_hoja = "documentos_detalles"
            nombre_archivo = "documentos_detalles.xlsx"
            if request.query_params.get('excel_masivo'):
                exporter = ExcelExportar(serializer.data, nombre_hoja, nombre_archivo)
                return exporter.exportar() 
            elif request.query_params.get('excel_informe'): 
                serializador_parametro = self.request.query_params.get('serializador', None)                
                if serializador_parametro == 'informe_venta':
                    titulo = 'Ventas por item' 
                    nombre_archivo = "ventas_por_item.xlsx"  
                exporter = ExcelExportar(serializer.data, nombre_hoja, nombre_archivo, titulo)
                return exporter.exportar_informe()                    
            else:
                exporter = ExcelExportar(serializer.data, nombre_hoja, nombre_archivo)
                return exporter.exportar_estilo()            
        return super().list(request, *args, **kwargs)

    def create(self, request):
        raw = request.data
        documentoDetalleSerializador = GenDocumentoDetalleSerializador(data=raw)
        if documentoDetalleSerializador.is_valid():
            documentoDetalleSerializador.save()            
            return Response({'documento': documentoDetalleSerializador.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': documentoDetalleSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path=r'agregar_documento')
    def agregarDocumentoDetalle(self, request): 
        limit = request.query_params.get('limit', 10)
        documento_tipo = request.query_params.get('documento_tipo', None)
        queryset = self.get_queryset()
        if documento_tipo:
            queryset = queryset.filter(documento__documento_tipo=documento_tipo)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = GenDocumentoDetalleAgregarDocumentoSerializador(queryset, many=True)        
        return Response(serializer.data)    
