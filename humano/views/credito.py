from rest_framework import viewsets, permissions
from humano.models.credito import HumCredito
from humano.serializers.credito import HumCreditoSerializador
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from humano.filters.credito import CreditoFilter
from utilidades.excel_exportar import ExcelExportar

class HumCreditoViewSet(viewsets.ModelViewSet):
    queryset = HumCredito.objects.all()
    serializer_class = HumCreditoSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CreditoFilter 

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return HumCreditoSerializador
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
            exporter = ExcelExportar(serializer.data, sheet_name="creditos", filename="creditos.xlsx")
            return exporter.export()
        return super().list(request, *args, **kwargs)   

    def perform_create(self, serializer):
        total = serializer.validated_data.get('total')
        serializer.save(saldo=total)

    def perform_update(self, serializer):
        total = serializer.validated_data.get('total')
        abono = serializer.validated_data.get('abono', serializer.instance.abono)
        saldo = total - abono
        serializer.save(saldo=saldo)