from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from transporte.models.negocio import TteNegocio
from vertical.models.viaje import VerViaje
from transporte.serializers.negocio import TteNegocioSerializador
from transporte.filters.negocio import NegocioFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from utilidades.excel_exportar import ExcelExportar
from django.db import transaction

class NegocioViewSet(viewsets.ModelViewSet):
    queryset = TteNegocio.objects.all()
    serializer_class = TteNegocioSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = NegocioFilter 
    serializadores = {
        'lista': TteNegocioSerializador,
    } 


    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return TteNegocioSerializador
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
        if request.query_params.get('lista_completa', '').lower() == 'true':
            self.pagination_class = None
        if request.query_params.get('excel'):   
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)         
            exporter = ExcelExportar(serializer.data, 'negocio', 'negocios.xlsx')
            return exporter.exportar_estilo()
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["post"], url_path=r'aprobar',)
    def aprobar_action(self, request):        
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                with transaction.atomic():
                    negocio = TteNegocio.objects.get(pk=id)
                    if negocio.estado_aprobado == False:
                        if negocio.publicar:
                            viaje = VerViaje()
                            viaje.negocio_id = id                            
                            viaje.peso = negocio.peso
                            viaje.volumen = negocio.volumen     
                            viaje.ciudad_origen_id = negocio.ciudad_origen_id
                            viaje.ciudad_destino_id = negocio.ciudad_destino_id                       
                            viaje.contenedor_id = request.tenant.id
                            viaje.schema_name = request.tenant.schema_name
                            viaje.save()  
                        negocio.estado_aprobado = True
                        negocio.save()
                        return Response({'estado_aprobado': True}, status=status.HTTP_200_OK)
                    else:
                        return Response({'mensaje':'El negocio ya se encuentra aprobado', 'codigo':16}, status=status.HTTP_400_BAD_REQUEST)
            except TteNegocio.DoesNotExist:
                return Response({'mensaje':'El negocio no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)