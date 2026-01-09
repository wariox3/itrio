from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from general.models.impuesto import GenImpuesto
from general.serializers.impuesto import GenImpuestoSerializador, GenImpuestoSeleccionarSerializador
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class ImpuestoViewSet(viewsets.ModelViewSet):
    queryset = GenImpuesto.objects.all()
    serializer_class = GenImpuestoSerializador
    permission_classes = [permissions.IsAuthenticated]  

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return GenImpuestoSerializador
        return self.serializadores[serializador_parametro]

    def get_queryset(self):
        self.pagination_class = PageNumberPagination
        self.pagination_class.page_size = 100
        queryset = super().get_queryset()
        serializer_class = self.get_serializer_class()        
        select_related = getattr(serializer_class.Meta, 'select_related_fields', [])
        if select_related:
            queryset = queryset.select_related(*select_related)        
        campos = serializer_class.Meta.fields        
        if campos and campos != '__all__':
            queryset = queryset.only(*campos) 
        return queryset 

    @action(detail=False, methods=["get"], url_path=r'seleccionar')
    def seleccionar_action(self, request):
        limit = request.query_params.get('limit', 20)
        nombre = request.query_params.get('nombre__icontains', None)
        venta = request.query_params.get('venta', None)
        compra = request.query_params.get('compra', None)
        queryset = self.get_queryset()
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if venta:
            queryset = queryset.filter(venta=venta)
        if compra:
            queryset = queryset.filter(compra=compra)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = GenImpuestoSeleccionarSerializador(queryset, many=True)        
        return Response(serializer.data)    