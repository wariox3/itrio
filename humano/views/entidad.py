from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.entidad import HumEntidad
from humano.serializers.entidad import HumEntidadSerializador, HumEntidadSeleccionarSerializador

class HumEntidadViewSet(viewsets.ModelViewSet):
    queryset = HumEntidad.objects.all()
    serializer_class = HumEntidadSerializador
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
        salud = request.query_params.get('salud', None)
        pension = request.query_params.get('pension', None)
        cesantias = request.query_params.get('cesantias', None)
        caja = request.query_params.get('caja', None)
        queryset = self.get_queryset()
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if salud:
            queryset = queryset.filter(salud=salud)
        if pension:
            queryset = queryset.filter(pension=pension)
        if cesantias:
            queryset = queryset.filter(cesantias=cesantias)
        if caja:
            queryset = queryset.filter(caja=caja)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = HumEntidadSeleccionarSerializador(queryset, many=True)        
        return Response(serializer.data)      