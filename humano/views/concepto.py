from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.concepto import HumConcepto
from humano.serializers.concepto import HumConceptoSerializador, HumConceptoSeleccionarSerializador

class HumConceptoViewSet(viewsets.ModelViewSet):
    queryset = HumConcepto.objects.all()
    serializer_class = HumConceptoSerializador
    permission_classes = [permissions.IsAuthenticated]

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

    @action(detail=False, methods=["get"], url_path=r'seleccionar')
    def seleccionar_action(self, request):
        limit = request.query_params.get('limit', 10)
        nombre = request.query_params.get('nombre__icontains', None)
        adicional = request.query_params.get('adicional', None)
        queryset = self.get_queryset()
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if adicional:
            queryset = queryset.filter(adicional=adicional)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = HumConceptoSeleccionarSerializador(queryset, many=True)        
        return Response(serializer.data)      