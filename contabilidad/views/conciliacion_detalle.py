from rest_framework import viewsets, permissions, status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.movimiento import ConMovimiento
from contabilidad.models.conciliacion import ConConciliacion
from contabilidad.models.conciliacion_detalle import ConConciliacionDetalle
from contabilidad.serializers.conciliacion_detalle import ConConciliacionDetalleSerializador
from contabilidad.filters.conciliacion_detalle import ConciliacionDetalleFilter
from utilidades.excel_exportar import ExcelExportar


class ConciliacionDetalleViewSet(viewsets.ModelViewSet):
    queryset = ConConciliacionDetalle.objects.all()
    serializer_class = ConConciliacionDetalleSerializador
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ConciliacionDetalleFilter 
    permission_classes = [permissions.IsAuthenticated]
    serializadores = {'lista': ConConciliacionDetalleSerializador}

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return ConConciliacionDetalleSerializador
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
            exporter = ExcelExportar(serializer.data, nombre_hoja="conciliaciones_detalles", nombre_archivo="conciliacionesDetalles.xlsx", titulo="ConciliacionesDetalles")            
            return exporter.exportar()
        return super().list(request, *args, **kwargs)    
           

    @action(detail=False, methods=["post"], url_path=r'cargar')
    def cargar(self, request):
        try:
            raw = request.data
            id = raw.get('conciliacion_id')
            if id:
                conciliacion = ConConciliacion.objects.get(pk=id)
                movimientos = ConMovimiento.objects.filter(
                    cuenta_id=conciliacion.cuenta_banco.cuenta,
                    fecha__gte=conciliacion.fecha_desde,
                    fecha__lte=conciliacion.fecha_hasta
                )
                
                for movimiento in movimientos:
                    data = {
                        'conciliacion': conciliacion.id,
                        'documento': movimiento.documento_id,
                        'cuenta': conciliacion.cuenta_banco.cuenta_id,
                        'debito': movimiento.debito,
                        'credito': movimiento.credito,
                        'fecha': movimiento.fecha,
                        'detalle': movimiento.detalle,
                    }

                    if movimiento.contacto_id:
                        data['contacto'] = movimiento.contacto_id

                    serializer = ConConciliacionDetalleSerializador(data=data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response({'errores': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                
                return Response({
                    'mensaje': f'Se cargaron los detalles con éxito'
                }, status=status.HTTP_200_OK)
                        
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)            
        except ConConciliacion.DoesNotExist:
            return Response({'mensaje':'La conciliación no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)