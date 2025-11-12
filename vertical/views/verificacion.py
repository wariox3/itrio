from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.verificacion import VerVerificacion
from vertical.models.verificacion_concepto import VerVerificacionConcepto
from vertical.models.verificacion_detalle import VerVerificacionDetalle
from vertical.models.vehiculo import VerVehiculo
from vertical.models.conductor import VerConductor
from vertical.serializers.verificacion import VerVerficacionSerializador
from vertical.serializers.verificacion_detalle import VerVerificacionDetalleSerializador
from django.db import transaction
from datetime import datetime, timedelta

class VerificacionViewSet(viewsets.ModelViewSet):
    queryset = VerVerificacion.objects.all()
    serializer_class = VerVerficacionSerializador
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=False, methods=["post"], url_path=r'nuevo',)
    def nuevo_action(self, request):        
        raw = request.data    
        verificacion_serializador = VerVerficacionSerializador(data=raw)
        if verificacion_serializador.is_valid():
            verificacion_tipo_id = raw.get('verificacion_tipo_id', raw)
            if verificacion_tipo_id == 1:
                vehiculo_id = raw.get('vehiculo', None)
                if vehiculo_id:
                    vehiculo = VerVehiculo.objects.get(pk=vehiculo_id)
                    if vehiculo.verificado:
                        return Response({'mensaje':'El vehiculo ya ha sido verificado', 'codigo':2}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje':'Faltan parametros: vehiculo', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
            elif verificacion_tipo_id == 2:
                conductor_id = raw.get('conductor', None)
                if conductor_id:
                    conductor = VerConductor.objects.get(pk=conductor_id)
                    if conductor.verificado:
                        return Response({'mensaje':'El conductor ya ha sido verificado', 'codigo':2}, status=status.HTTP_400_BAD_REQUEST)
                else:                
                    return Response({'mensaje':'Faltan parametros: conductor', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
            verificacion = verificacion_serializador.save()
            return Response({'mensaje': 'Verificacion creada', 'verificacion': verificacion_serializador.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'mensaje': 'Error al crear el verificacion', 'validaciones': verificacion_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)        

    @action(detail=False, methods=["post"], url_path=r'proceso',)
    def proceso_action(self, request):        
        raw = request.data    
        id = raw.get('id', None)
        if id:
            try:
                verificacion = VerVerificacion.objects.get(pk=id)
            except VerVerificacion.DoesNotExist:
                return Response({'mensaje':'La verificacion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)            
            if verificacion:
                if verificacion.estado_proceso:
                    return Response({'mensaje':'La verificacion ya ha sido procesada', 'codigo':4}, status=status.HTTP_400_BAD_REQUEST)
                with transaction.atomic():
                    verificacion.estado_proceso = True
                    verificacion.save()
                    if verificacion.verificacion_tipo_id == 1:
                        vehiculo = verificacion.vehiculo
                        vehiculo.verificado_proceso = True                        
                        vehiculo.save()
                        verificacion_conceptos = VerVerificacionConcepto.objects.filter(verificacion_tipo_id=1)
                        for concepto in verificacion_conceptos:
                            data = {
                                'verificacion': verificacion.id,
                                'verificacion_concepto': concepto.id
                            }
                            verificacion_detalle_serializador = VerVerificacionDetalleSerializador(data=data)
                            if verificacion_detalle_serializador.is_valid():
                                verificacion_detalle_serializador.save()
                        return Response({'mensaje':'Verificacion de vehiculo procesada correctamente', 'codigo':0}, status=status.HTTP_200_OK)
                    elif verificacion.verificacion_tipo_id == 2:
                        conductor = verificacion.conductor
                        conductor.verificado_proceso = True                                            
                        conductor.save()
                        return Response({'mensaje':'Verificacion de conductor procesada correctamente', 'codigo':0}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':'La verificacion no existe', 'codigo':3}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros: id', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], url_path=r'verificar',)
    def verificar_action(self, request):        
        raw = request.data    
        id = raw.get('id', None)
        if id:
            try:
                verificacion = VerVerificacion.objects.get(pk=id)
            except VerVerificacion.DoesNotExist:
                return Response({'mensaje':'La verificacion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)            
            if verificacion:
                if not verificacion.estado_proceso:
                    return Response({'mensaje':'La verificacion debe estar en proceso', 'codigo':4}, status=status.HTTP_400_BAD_REQUEST)
                if verificacion.verificado:
                    return Response({'mensaje':'La verificacion ya esta verificada', 'codigo':4}, status=status.HTTP_400_BAD_REQUEST)                
                verificanes_detalles = VerVerificacionDetalle.objects.filter(verificacion=verificacion, verificado=False).first()
                if verificanes_detalles:
                    return Response({'mensaje':'Existen detalles no verificados', 'codigo':5}, status=status.HTTP_400_BAD_REQUEST)
                with transaction.atomic():                        
                    fecha_actual = datetime.now().date()
                    fecha_vence = fecha_actual + timedelta(days=30)
                    verificacion.verificado = True
                    verificacion.fecha_verificacion = fecha_actual
                    verificacion.fecha_verificacion_vence = fecha_vence
                    verificacion.save()
                    if verificacion.verificacion_tipo_id == 1:
                        vehiculo = verificacion.vehiculo
                        vehiculo.verificado = True  
                        vehiculo.fecha_verificacion = fecha_actual
                        vehiculo.fecha_verificacion_vence = fecha_vence
                        vehiculo.save()
                    return Response({'mensaje':'Verificacion procesada correctamente', 'codigo':0}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':'La verificacion no existe', 'codigo':3}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros: id', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)        
   