from rest_framework import viewsets, permissions
from general.models.plazo_pago import PlazoPago
from general.serializers.plazo_pago import PlazoPagoSerializador
from rest_framework.decorators import action
from rest_framework.response import Response

class PlazoPagoViewSet(viewsets.ModelViewSet):
    queryset = PlazoPago.objects.all()
    serializer_class = PlazoPagoSerializador    
    permission_classes = [permissions.IsAuthenticated]        

'''@action(detail=False, methods=["post"], url_path=r'lista',)
def lista(self, request):
    raw = request.data
    desplazar = raw.get('desplazar', 0)
    limite = raw.get('limite', 50)    
    cantidadLimite = raw.get('cantidad_limite', 5000)    
    filtros = raw.get('filtros')
    ordenamientos = raw.get('ordenamientos')
    plazoPagos = PlazoPago.objects.all()
    if filtros:
        for filtro in filtros:
            plazoPagos = plazoPagos.filter(**{filtro['propiedad']: filtro['valor1']})
    if ordenamientos:
        plazoPagos = plazoPagos.order_by(*ordenamientos)              
    plazoPagos = plazoPagos[desplazar:limite+desplazar]
    plazoCantidad = PlazoPago.objects.all()[:cantidadLimite].count()
    ItemSerializador = ItemSerializador(plazoPagos, many=True)
    return Response({"registros": ItemSerializador.data, "cantidad_registros": plazoCantidad}, status=status.HTTP_200_OK)'''