from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from general.models.documento_tipo import GenDocumentoTipo
from general.models.resolucion import GenResolucion
from general.serializers.documento_tipo import GenDocumentoTipoSerializador, GenDocumentoTipoAutocompletarSerializador
from general.filters.documento_tipo import DocumentoTipoFilter
from utilidades.excel_exportar import ExcelExportar

class DocumentoTipoViewSet(viewsets.ModelViewSet):
    queryset = GenDocumentoTipo.objects.all().order_by('id')
    serializer_class = GenDocumentoTipoSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DocumentoTipoFilter 
    serializadores = {'autocompletar': GenDocumentoTipoAutocompletarSerializador}

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return GenDocumentoTipoSerializador
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
    
    def create(self, request, *args, **kwargs):
        return Response({'mensaje': 'No es posible crear un registro nuevo'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path=r'asignar-resolucion')
    def asignar_resolucion(self, request):
        raw = request.data
        resolucion_id = raw.get('resolucion_id')
        if resolucion_id:
            try:                
                documento_tipo = GenDocumentoTipo.objects.get(pk=1)
                if documento_tipo.resolucion_id == None:
                    resolucion = GenResolucion.objects.get(pk=resolucion_id)
                    documento_tipo.resolucion = resolucion
                    documento_tipo.save()                
                    return Response({'asignado': True}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje': 'El documento ya tiene resolucion', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)  
            except GenResolucion.DoesNotExist:
                return Response({'mensaje':'La resolucion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                         
        else:
            return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)              
                        
       