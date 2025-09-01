from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.producto import VerProducto
from vertical.serializers.producto import VerProductoSerializador, VerProductoSeleccionarSerializador

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = VerProducto.objects.all()
    serializer_class = VerProductoSerializador
    permission_classes = [permissions.IsAuthenticated]

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
        serializer = VerProductoSeleccionarSerializador(queryset, many=True)        
        return Response(serializer.data)    