from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from general.models.impuesto import GenImpuesto
from general.serializers.impuesto import GenImpuestoSerializador, GenImpuestoSeleccionarSerializador
from rest_framework.response import Response

class ImpuestoViewSet(viewsets.ModelViewSet):
    queryset = GenImpuesto.objects.all()
    serializer_class = GenImpuestoSerializador
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        queryset = super().get_queryset()               
        select_related = getattr(self.serializer_class.Meta, 'select_related_fields', [])
        if select_related:
            queryset = queryset.select_related(*select_related)        
        campos = self.serializer_class.Meta.fields        
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