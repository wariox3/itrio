from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from general.models.documento_guia import GenDocumentoGuia
from general.serializers.documento_guia import GenDocumentoGuiaSerializador
from general.filters.documento_guia import DocumentoGuiaFilter
from rest_framework.decorators import action

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



    