from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.verificacion_detalle import VerVerificacionDetalle
from vertical.serializers.verificacion_detalle import VerVerificacionDetalleSerializador
from django.db import transaction
from datetime import datetime, timedelta
class VerificacionDetalleViewSet(viewsets.ModelViewSet):
    queryset = VerVerificacionDetalle.objects.all()
    serializer_class = VerVerificacionDetalleSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'verificar',)
    def verificar_action(self, request):        
        raw = request.data    
        id = raw.get('id', None)
        if id:
            try:
                verificacion_detalle = VerVerificacionDetalle.objects.get(pk=id)
            except VerVerificacionDetalle.DoesNotExist:
                return Response({'mensaje':'La verificacion detalle no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)            
            if verificacion_detalle:
                if verificacion_detalle.verificado:
                    return Response({'mensaje':'La verificacion detalle ya esta verificada', 'codigo':4}, status=status.HTTP_400_BAD_REQUEST)                
                with transaction.atomic():                        
                    fecha_actual = datetime.now().date()
                    verificacion_detalle.verificado = True        
                    verificacion_detalle.save()
                    return Response({'mensaje':'Verificacion detalle procesada correctamente', 'codigo':0}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':'La verificacion detalle no existe', 'codigo':3}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros: id', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)        
   