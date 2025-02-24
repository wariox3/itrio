from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.periodo import ConPeriodo
from contabilidad.models.movimiento import ConMovimiento
from contabilidad.serializers.periodo import ConPeriodoSerializador
from django.db.models import Sum

class PeriodoViewSet(viewsets.ModelViewSet):
    queryset = ConPeriodo.objects.all()
    serializer_class = ConPeriodoSerializador
    permission_classes = [permissions.IsAuthenticated]  

    @staticmethod
    def analizar_inconsistencias(id):
        movimientos = ConMovimiento.objects.filter(
            periodo=id
            ).values(
                'comprobante_id', 
                'numero'
            ).annotate(
            total_debito=Sum('debito'),
            total_credito=Sum('credito')
        )        
        return None

    @action(detail=False, methods=["get"], url_path=r'anio',)
    def anio(self, request):
        periodos = ConPeriodo.objects.values_list('anio', flat=True).distinct()
        return Response({'anios': periodos}, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=["post"], url_path=r'anio-nuevo',)
    def anio_nuevo(self, request):
        raw = request.data        
        anio = raw.get('anio')
        if anio:
            periodo = ConPeriodo.objects.filter(anio=anio).first()
            if periodo is None:
                for i in range(1, 14):
                    codigo = f"{anio}{str(i).zfill(2)}"
                    ConPeriodo.objects.create(id=codigo, anio=anio, mes=i)
                return Response({'mensaje': 'Se generan los periodos del año'}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje': 'Ya existen periodos con este año'}, status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
        
    @action(detail=False, methods=["post"], url_path=r'bloquear',)
    def bloquear(self, request):
        raw = request.data        
        id = raw.get('id')
        if id:
            periodo = ConPeriodo.objects.get(pk=id)
            if periodo:
                if not periodo.estado_bloqueado:
                    periodo.estado_bloqueado = True
                    periodo.save()
                    return Response({'mensaje': 'Periodo bloqueado'}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje': 'El periodo ya estaba bloqueado previamente'}, status=status.HTTP_400_BAD_REQUEST)    
            else:
                return Response({'mensaje': 'No existe el periodo'}, status=status.HTTP_400_BAD_REQUEST)                
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)         
        
    @action(detail=False, methods=["post"], url_path=r'desbloquear',)
    def desbloquear(self, request):
        raw = request.data        
        id = raw.get('id')
        if id:
            periodo = ConPeriodo.objects.get(pk=id)
            if periodo:
                if periodo.estado_bloqueado:
                    if not periodo.estado_cerrado:
                        periodo.estado_bloqueado = False
                        periodo.save()
                        return Response({'mensaje': 'Periodo desbloqueado'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'mensaje': 'El periodo esta cerrado y no se puede desbloquear'}, status=status.HTTP_400_BAD_REQUEST)        
                else:
                    return Response({'mensaje': 'El periodo no esta bloqueado'}, status=status.HTTP_400_BAD_REQUEST)    
            else:
                return Response({'mensaje': 'No existe el periodo'}, status=status.HTTP_400_BAD_REQUEST)                
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    

    @action(detail=False, methods=["post"], url_path=r'cerrar',)
    def cerrar(self, request):
        raw = request.data        
        id = raw.get('id')
        if id:
            periodo = ConPeriodo.objects.get(pk=id)
            if periodo:
                if periodo.estado_bloqueado == True:
                    if not periodo.estado_cerrado:
                        periodo.estado_cerrado = True
                        periodo.save()
                        return Response({'mensaje': 'Periodo cerrado'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'mensaje': 'El periodo ya estaba cerrado previamente'}, status=status.HTTP_400_BAD_REQUEST)    
                else:
                    return Response({'mensaje': 'El periodo debe estar bloqueado para cerrar'}, status=status.HTTP_400_BAD_REQUEST)                    
            else:
                return Response({'mensaje': 'No existe el periodo'}, status=status.HTTP_400_BAD_REQUEST)                
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)   

    @action(detail=False, methods=["post"], url_path=r'inconsistencia',)
    def inconsistencia(self, request):
        raw = request.data        
        id = raw.get('id')
        if id:
            periodo = ConPeriodo.objects.get(pk=id)
            if periodo:            
                self.analizar_inconsistencias(id)    
                return Response({'mensaje': 'Inconsistencia'}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje': 'No existe el periodo'}, status=status.HTTP_400_BAD_REQUEST)                
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                  