from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from transporte.models.despacho import TteDespacho
from transporte.models.guia import TteGuia
from transporte.serializers.despacho import TteDespachoSerializador
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
        if request.query_params.get('lista', '').lower() == 'true':
            self.pagination_class = None
        return super().list(request, *args, **kwargs)    
    
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
            if guia.estado_despachado == False:  
                with transaction.atomic():   
                    guia.despacho = despacho
                    guia.estado_despachado = True
                    guia.save()
                    TteDespacho.objects.filter(pk=id).update(guias=F('guias') + 1)  
                    return Response({'mensaje': f'Guia adicionada al despaho'}, status=status.HTTP_200_OK)                  
            else:
                return Response({'mensaje':'La guia ya esta despachada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    