from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from general.models.precio_detalle import GenPrecioDetalle
from general.serializers.precio_detalle import GenPrecioDetalleSerializador
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from general.filters.precio_detalle import PrecioDetalleFilter
from rest_framework.response import Response

class PrecioDetalleViewSet(viewsets.ModelViewSet):
    queryset = GenPrecioDetalle.objects.all()
    serializer_class = GenPrecioDetalleSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]    
    filterset_class = PrecioDetalleFilter 
    serializadores = {
        'lista': GenPrecioDetalleSerializador
    }

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return GenPrecioDetalleSerializador
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
        if request.query_params.get('lista', '').lower() == 'true':
            self.pagination_class = None
        return super().list(request, *args, **kwargs)    
    

    @action(detail=False, methods=["get"], url_path=r'consultar_precio')
    def consultar_precio(self, request):
        precio_id = request.query_params.get('precio_id', None)
        item_id = request.query_params.get('item_id', None)
        
        if precio_id and item_id:        
            try:
                precio_detalle = GenPrecioDetalle.objects.filter(precio_id=precio_id,item_id=item_id).order_by('id').first()
                if precio_detalle:
                    return Response({'vr_precio': precio_detalle.vr_precio}, status=status.HTTP_200_OK)
                else:
                    return Response({'vr_precio': None}, status=status.HTTP_200_OK)
                
            except Exception as e:
                return Response({'mensaje': 'Error procesando la api', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)              
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                