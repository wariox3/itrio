from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.propuesta import VerPropuesta
from vertical.models.viaje import VerViaje
from vertical.serializers.propuesta import VerPropuestaSerializador
from django.db import transaction
from django.db.models import Sum, Count, F
from django.db.models import Prefetch

class PropuestaViewSet(viewsets.ModelViewSet):
    queryset = VerPropuesta.objects.all()
    serializer_class = VerPropuestaSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'adicionar-propuesta',)
    def adicionar_propuesta_action(self, request):                     
        raw = request.data
        viaje_id = raw.get('viaje_id')           
        precio = raw.get('precio')  
        empresa = raw.get('empresa')        
        if viaje_id and precio and empresa:
            try:
                viaje = VerViaje.objects.get(pk=viaje_id)
            except VerViaje.DoesNotExist:
                return Response({'mensaje':'El viaje no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
         
            if viaje.estado_aceptado == False:  
                existe_propuesta = VerPropuesta.objects.filter(viaje_id=viaje_id, usuario_id=request.user.id).exists()
                if existe_propuesta:
                    return Response({'mensaje':'Ya existe una propuesta de este usuario para este viaje', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                
                with transaction.atomic():  
                    tenant = request.tenant                                       
                    data = {
                        'viaje':viaje_id,
                        'precio':precio,    
                        'usuario': request.user.id, 
                        'contenedor_id': tenant.id,
                        'schema_name': tenant.schema_name,
                        'empresa': empresa               
                    }
                    propuesta_serializador = VerPropuestaSerializador(data=data)
                    if propuesta_serializador.is_valid():    
                        propuesta_serializador.save()     
                        VerViaje.objects.filter(pk=viaje_id).update(propuestas=F('propuestas') + 1)                                             
                    else:
                        return Response({'validaciones': propuesta_serializador.errors, 'mensaje': 'No se pudo crear la propuesta'}, status=status.HTTP_400_BAD_REQUEST)                        

                    return Response({'mensaje': f'Guia adicionada al despacho'}, status=status.HTTP_200_OK)                  
            else:
                return Response({'mensaje':'El viaje ya esta aceptado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

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
                    viaje.pago = propuesta.pago
                    viaje.estado_aceptado = True
                    viaje.contenedor_negocio_id = propuesta.contenedor_id
                    viaje.save()
                    propuestas_serializador = VerPropuestaSerializador(propuesta)
                    return Response({'mensaje': 'propuesta aceptada', 'propuesta': propuestas_serializador.data}, status=status.HTTP_200_OK) 
                else:
                    return Response({'mensaje':'La propuesta ya fue aceptada con anterioridad', 'codigo':16}, status=status.HTTP_400_BAD_REQUEST)                                                                                                           

        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    

       