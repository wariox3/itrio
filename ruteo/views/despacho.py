from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ruteo.models.despacho import RutDespacho
from ruteo.models.visita import RutVisita
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

    def destroy(self, request, *args, **kwargs):        
        instance = self.get_object()
        if instance.estado_aprobado:
                return Response({'mensaje': 'No se puede eliminar un despacho aprobado.'}, status=status.HTTP_400_BAD_REQUEST)        
        RutVisita.objects.filter(despacho_id=instance.id).update(despacho=None, estado_despacho=False)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)    
             