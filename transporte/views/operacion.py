from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from transporte.models.operacion import TteOperacion
from transporte.serializers.operacion import TteOperacionSerializador, TteOpercionSeleccionarSerializador
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class OperacionViewSet(viewsets.ModelViewSet):
    queryset = TteOperacion.objects.all()
    serializer_class = TteOperacionSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]

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
        serializer = TteOpercionSeleccionarSerializador(queryset, many=True)        
        return Response(serializer.data)        