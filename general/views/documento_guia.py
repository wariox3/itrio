from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from general.models.documento import GenDocumento
from general.models.documento_guia import GenDocumentoGuia
from transporte.models.guia import TteGuia
from general.serializers.documento_guia import GenDocumentoGuiaSerializador
from general.filters.documento_guia import DocumentoGuiaFilter
from rest_framework.decorators import action
from django.db import transaction
from django.db.models import Sum, F, Count

class DocumentoGuiaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter] 
    filterset_class = DocumentoGuiaFilter
    queryset = GenDocumentoGuia.objects.all()
    serializadores = {
        'lista': GenDocumentoGuiaSerializador,
    }
    
    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return GenDocumentoGuiaSerializador
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

    @action(detail=False, methods=["post"], url_path=r'adicionar-guia',)
    def adicionar_guia_action(self, request):                     
        raw = request.data
        documento_id = raw.get('documento_id')           
        guia_id = raw.get('guia_id')           
        if documento_id and guia_id:
            try:
                documento = GenDocumento.objects.get(pk=documento_id)
            except GenDocumento.DoesNotExist:
                return Response({'mensaje':'El documento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
            try:
                guia = TteGuia.objects.get(pk=guia_id)                            
            except TteGuia.DoesNotExist:
                return Response({'mensaje':'La guia no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)           
            if guia.estado_facturado == False and guia.factura_id == None:  
                with transaction.atomic():   
                    data = {
                        'documento':documento_id,
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
                    serializador_documento_guia = GenDocumentoGuiaSerializador(data=data)
                    if serializador_documento_guia.is_valid():    
                        serializador_documento_guia.save()                        
                    else:
                        return Response({'validaciones': serializador_documento_guia.errors, 'mensaje': 'Errores en la creacion de documento guia'}, status=status.HTTP_400_BAD_REQUEST)                        
                    guia.factura = documento
                    guia.estado_facturado = True
                    guia.save()
                    GenDocumento.objects.filter(pk=documento_id).update(guias=F('guias') + 1)  
                    return Response({'mensaje': f'Guia adicionada al despacho'}, status=status.HTTP_200_OK)                  
            else:
                return Response({'mensaje':'La guia ya esta facturada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], url_path=r'eliminar',)
    def eliminar_action(self, request):                     
        raw = request.data
        id = raw.get('id')                             
        if id:
            try:
                documento_guia = GenDocumentoGuia.objects.get(pk=id)
            except GenDocumentoGuia.DoesNotExist:
                return Response({'mensaje':'El documento guia no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 
            try:
                guia = TteGuia.objects.get(pk=documento_guia.guia_id)                            
            except TteGuia.DoesNotExist:
                return Response({'mensaje':'La guia no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                      
            if documento_guia.documento.estado_aprobado == False:  
                with transaction.atomic():   
                    documento_guia.delete()                    
                    guia.factura = None
                    guia.estado_facturado = False
                    guia.save()
                    GenDocumento.objects.filter(pk=documento_guia.documento_id).update(guias=F('guias') - 1)  
                    return Response({'mensaje': f'Guia eliminada del despacho'}, status=status.HTTP_200_OK)                  
            else:
                return Response({'mensaje':'La factura ya esta aprobada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)          


    