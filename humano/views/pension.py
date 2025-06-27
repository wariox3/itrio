from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.pension import HumPension
from humano.serializers.pension import HumPensionSerializador, HumPensionSeleccionarSerializador

class HumPensionViewSet(viewsets.ModelViewSet):
    queryset = HumPension.objects.all()
    serializer_class = HumPensionSerializador
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
        queryset = self.get_queryset()
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = HumPensionSeleccionarSerializador(queryset, many=True)        
        return Response(serializer.data)      