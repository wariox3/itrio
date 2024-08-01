from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ruteo.models.despacho import RutDespacho
from ruteo.serializers.despacho import RutDespachoSerializador

def listar(desplazar, limite, limiteTotal, filtros, ordenamientos):
    despachos = RutDespacho.objects.all()
    if filtros:
        for filtro in filtros:
            despachos = despachos.filter(**{filtro['propiedad']: filtro['valor1']})
    if ordenamientos:
        despachos = despachos.order_by(*ordenamientos)              
    despachos = despachos[desplazar:limite+desplazar]
    itemsCantidad = RutDespacho.objects.all()[:limiteTotal].count()                   
    respuesta = {'despachos': despachos, "cantidad_registros": itemsCantidad}
    return respuesta 

class RutDespachoViewSet(viewsets.ModelViewSet):
    queryset = RutDespacho.objects.all()
    serializer_class = RutDespachoSerializador
    permission_classes = [permissions.IsAuthenticated]      


    @action(detail=False, methods=["post"], url_path=r'lista',)
    def lista(self, request):
        raw = request.data
        desplazar = raw.get('desplazar', 0)
        limite = raw.get('limite', 50)    
        limiteTotal = raw.get('limite_total', 5000)                
        ordenamientos = raw.get('ordenamientos', [])            
        filtros = raw.get('filtros', [])                   
        respuesta = listar(desplazar, limite, limiteTotal, filtros, ordenamientos)     
        serializador = RutDespachoSerializador(respuesta['despachos'], many=True)
        visitas = serializador.data
        return Response(visitas, status=status.HTTP_200_OK)               