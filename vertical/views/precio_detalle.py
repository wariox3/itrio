from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.precio_detalle import VerPrecioDetalle
from vertical.serializers.precio_detalle import VerPrecioDetalleSerializador
from vertical.filters.precio_detalle import VerPrecioDetalleFilter
from django.db import transaction
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class PrecioDetalleViewSet(viewsets.ModelViewSet):
    queryset = VerPrecioDetalle.objects.all()
    serializer_class = VerPrecioDetalleSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = VerPrecioDetalleFilter
    serializadores = {
        'lista': VerPrecioDetalleSerializador,
    } 

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return VerPrecioDetalleSerializador
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
            exporter = ExcelExportar(serializer.data, nombre_hoja="despachos", nombre_archivo="despachos.xlsx", titulo="Despachos")
            if request.query_params.get('excel'):
                return exporter.exportar_estilo()
            if request.query_params.get('excel_masivo'):
                return exporter.exportar()
        return super().list(request, *args, **kwargs)       