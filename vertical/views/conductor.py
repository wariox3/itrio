from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.conductor import VerConductor
from vertical.serializers.conductor import VerConductorSerializador, VerConductorVerificarSerializador
from django.db import transaction

class ConductorViewSet(viewsets.ModelViewSet):
    queryset = VerConductor.objects.all()
    serializer_class = VerConductorSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'verificar',)
    def verificar_action(self, request):        
        raw = request.data
        numero_identificacion = raw.get('numero_identificacion', raw)
        if numero_identificacion:
            #with transaction.atomic():
            conductor = VerConductor.objects.filter(numero_identificacion=numero_identificacion).first()
            if conductor:
                if conductor.verificado:
                    # Fecha de vencimiento de la licencia
                    coductor_serializador = VerConductorVerificarSerializador(conductor)
                    return Response({'conductor': coductor_serializador.data}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'El conductor no ha sido verificado en los servicio de RedDoc', 'codigo':2}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje':'El conductor no esta registrado en los servicio de RedDoc', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                 
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
        
   