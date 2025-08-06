from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from transporte.models.negocio import TteNegocio
from transporte.serializers.negocio import TteNegocioSerializador
from transporte.filters.negocio import NegocioFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

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
        if request.query_params.get('lista', '').lower() == 'true':
            self.pagination_class = None
        return super().list(request, *args, **kwargs)    