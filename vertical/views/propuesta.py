from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.propuesta import VerPropuesta
from vertical.models.vehiculo import VerVehiculo
from vertical.models.conductor import VerConductor
from vertical.serializers.propuesta import VerPropuestaSerializador
from django.db import transaction

class PropuestaViewSet(viewsets.ModelViewSet):
    queryset = VerPropuesta.objects.all()
    serializer_class = VerPropuestaSerializador
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=False, methods=["post"], url_path=r'aceptar',)
    def aceptar_action(self, request):        
        raw = request.data
        id = raw.get('id')
        if id:            
            with transaction.atomic():
                try:
                    propuesta = VerPropuesta.objects.get(pk=id)
                except VerPropuesta.DoesNotExist:
                    return Response({'mensaje':'La propuesta no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
                                
                if propuesta.estado_aceptado == False:                   
                    propuesta.estado_aceptado = True
                    propuesta.save()                    
                    viaje = propuesta.viaje
                    viaje.flete = propuesta.precio
                    viaje.estado_aceptado = True
                    viaje.contenedor_negocio_id = propuesta.contenedor_id
                    viaje.save()
                    return Response({'mensaje': 'propuesta aceptada'}, status=status.HTTP_200_OK) 
                else:
                    return Response({'mensaje':'La propuesta ya fue aceptada con anterioridad', 'codigo':16}, status=status.HTTP_400_BAD_REQUEST)                                                                                                           

        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)     