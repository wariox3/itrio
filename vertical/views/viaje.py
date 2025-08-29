from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.viaje import VerViaje
from vertical.models.vehiculo import VerVehiculo
from vertical.models.conductor import VerConductor
from vertical.serializers.viaje import VerViajeSerializador
from django.db import transaction

class ViajeViewSet(viewsets.ModelViewSet):
    queryset = VerViaje.objects.all()
    serializer_class = VerViajeSerializador
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=False, methods=["post"], url_path=r'aceptar',)
    def aceptar_action(self, request):        
        raw = request.data
        viaje_id = raw.get('viaje_id')
        conductor_id = raw.get('conductor_id')
        vehiculo_id = raw.get('vehiculo_id')
        if viaje_id and conductor_id and vehiculo_id:            
            with transaction.atomic():
                try:
                    viaje = VerViaje.objects.get(pk=viaje_id)
                except VerViaje.DoesNotExist:
                    return Response({'mensaje':'El viaje no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
                if viaje.estado_aceptado:
                    return Response({'mensaje':'El viaje ya fue aceptado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                               
                try:
                    vehiculo = VerVehiculo.objects.get(pk=vehiculo_id)
                except VerVehiculo.DoesNotExist:
                    return Response({'mensaje':'El vehiculo no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    conductor = VerConductor.objects.get(pk=conductor_id)                                    
                except VerConductor.DoesNotExist:
                    return Response({'mensaje':'El conductor no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                                                                                                            
                viaje.conductor = conductor
                viaje.vehiculo = vehiculo
                viaje.estado_aceptado = True
                viaje.save()
                return Response({'mensaje': 'viaje aceptado'}, status=status.HTTP_200_OK) 
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)     