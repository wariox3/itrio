from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ruteo.models.despacho import RutDespacho
from ruteo.models.visita import RutVisita
from ruteo.serializers.despacho import RutDespachoSerializador

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
    
    @action(detail=False, methods=["post"], url_path=r'aprobar',)
    def aprobar(self, request):             
        raw = request.data
        id = raw.get('id')
        if id:
            try:                
                despacho = RutDespacho.objects.get(pk=id)  
                if despacho.estado_aprobado == False:
                    despacho.estado_aprobado = True                
                    despacho.save()               
                    return Response({'mensaje': 'Se aprobo el despacho'}, status=status.HTTP_200_OK)                
                else:
                    return Response({'mensaje':'El despacho ya esta aprobado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                        
            except RutDespacho.DoesNotExist:
                return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)     
             