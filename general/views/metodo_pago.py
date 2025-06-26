from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from general.models.metodo_pago import GenMetodoPago
from general.serializers.metodo_pago import GenMetodoPagoSerializador, GenMetodoPagoListaSerializador
from general.filters.metodo_pago import MetodoPagoFilter
from utilidades.excel_exportar import ExcelExportar
from rest_framework.response import Response

class MetodoPagoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MetodoPagoFilter 
    queryset = GenMetodoPago.objects.all()   
    serializer_class = GenMetodoPagoSerializador
    pagination_class = None



    def get_queryset(self):
        queryset = super().get_queryset()               
        select_related = getattr(self.serializer_class.Meta, 'select_related_fields', [])
        if select_related:
            queryset = queryset.select_related(*select_related)        
        campos = self.serializer_class.Meta.fields        
        if campos and campos != '__all__':
            queryset = queryset.only(*campos)     
        return queryset 
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        limit = request.query_params.get('limit')
        if limit and limit.isdigit():
            queryset = queryset[:int(limit)]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)   