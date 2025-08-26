from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from transporte.models.despacho import TteDespacho
from transporte.models.despacho_detalle import TteDespachoDetalle
from transporte.models.guia import TteGuia
from transporte.serializers.despacho import TteDespachoSerializador
from transporte.serializers.despacho_detalle import TteDespachoDetalleSerializador
from transporte.filters.despacho import DespachoFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.db.models import Sum, Count, F

class DespachoViewSet(viewsets.ModelViewSet):
    queryset = TteDespacho.objects.all()
    serializer_class = TteDespachoSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DespachoFilter 
    serializadores = {
        'lista': TteDespachoSerializador,
    } 

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return TteDespachoSerializador
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
        if request.query_params.get('excel') or request.query_params.get('excel_masivo'):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            exporter = ExcelExportar(serializer.data, nombre_hoja="despachos", nombre_archivo="contdespachosactos.xlsx", titulo="Despachos")
            if request.query_params.get('excel'):
                return exporter.exportar_estilo()
            if request.query_params.get('excel_masivo'):
                return exporter.exportar()
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=["post"], url_path=r'aprobar',)
    def aprobar_action(self, request):        
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                with transaction.atomic():
                    despacho = TteDespacho.objects.get(pk=id)                
                    despacho_detalles = TteDespachoDetalle.objects.filter(despacho_id=id)
                    respuesta = self.validacion_aprobar(despacho, despacho_detalles)
                    if respuesta['error'] == False:                                                                      
                        despacho.estado_aprobado = True
                        despacho.save()
                        return Response({'estado_aprobado': True}, status=status.HTTP_200_OK)
                    else:
                        return Response({'mensaje':respuesta['mensaje'], 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
            except TteDespacho.DoesNotExist:
                return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'adicionar-guia',)
    def adicionar_guia_action(self, request):                     
        raw = request.data
        id = raw.get('id')           
        guia_id = raw.get('guia_id')           
        if id and guia_id:
            try:
                despacho = TteDespacho.objects.get(pk=id)
            except TteDespacho.DoesNotExist:
                return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
            try:
                guia = TteGuia.objects.get(pk=guia_id)                            
            except TteGuia.DoesNotExist:
                return Response({'mensaje':'La guia no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)           
            if guia.estado_despachado == False and guia.despacho_id == None:  
                with transaction.atomic():   
                    data = {
                        'despacho':id,
                        'guia':guia_id,
                        'unidades': guia.unidades, 
                        'peso': guia.peso, 
                        'volumen': guia.volumen, 
                        'peso_facturado': guia.peso_facturado, 
                        'costo': guia.costo, 
                        'declara': guia.declara,                         
                        'flete':guia.flete, 
                        'manejo':guia.manejo, 
                        'recaudo':guia.recaudo, 
                        'cobro_entrega':guia.cobro_entrega                        
                    }
                    serializador = TteDespachoDetalleSerializador(data=data)
                    if serializador.is_valid():    
                        serializador.save()                        
                    else:
                        return Response({'validaciones': serializador.errors, 'mensaje': 'Cuenta por pagar'}, status=status.HTTP_400_BAD_REQUEST)                        
                    guia.despacho = despacho
                    guia.estado_despachado = True
                    guia.save()
                    TteDespacho.objects.filter(pk=id).update(guias=F('guias') + 1)  
                    return Response({'mensaje': f'Guia adicionada al despacho'}, status=status.HTTP_200_OK)                  
            else:
                return Response({'mensaje':'La guia ya esta despachada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
        
    @staticmethod
    def validacion_aprobar(despacho: TteDespacho, despacho_destalles: TteDespachoDetalle):
        if despacho.estado_aprobado == False:  
            if despacho_destalles:       
                for despacho_detalle in despacho_destalles:
                    pass
                return {'error':False}                    
            else:
                return {'error':True, 'mensaje':'El despacho no tiene guias', 'codigo':1}  
        else:
            return {'error':True, 'mensaje':'El despacho ya esta aprobado', 'codigo':1}          