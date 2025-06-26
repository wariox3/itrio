from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from contabilidad.models.comprobante import ConComprobante
from contabilidad.serializers.comprobante import ConComprobanteSerializador, ConComprobanteSeleccionarSerializar


class ComprobanteViewSet(viewsets.ModelViewSet):
    queryset = ConComprobante.objects.all()
    serializer_class = ConComprobanteSerializador
    permission_classes = [permissions.IsAuthenticated]
  
    @action(detail=False, methods=["get"], url_path=r'seleccionar')
    def seleccionar_action(self, request):
        limit = request.query_params.get('limit')
        nombre = request.query_params.get('nombre__icontains', None)
        permite_asiento = request.query_params.get('permite_asiento', None)
        queryset = self.get_queryset()
        if nombre:
            queryset = queryset.filter(nombre=nombre)
        if permite_asiento:
            queryset = queryset.filter(permite_asiento=permite_asiento)
        try:
            if limit:
                limit = int(limit)
                queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = ConComprobanteSeleccionarSerializar(queryset, many=True)        
        return Response(serializer.data)    
  