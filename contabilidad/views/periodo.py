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
        inconsistencias = []
        for movimiento in movimientos:
            diferencia = movimiento['total_debito'] - movimiento['total_credito']
            if diferencia > 1 or diferencia < -1:
                inconsistencias.append({
                    'comprobante_id': movimiento['comprobante_id'],
                    'numero': movimiento['numero'],
                    'cuenta_id': None,
                    'inconsistencia': 'El total de debito y credito no coinciden'
                })
        movimientos = ConMovimiento.objects.filter(
            periodo=id
            ).values(
                'comprobante_id',
                'numero',
                'cuenta_id',
                'grupo_id',
                'contacto_id',
                'base',
                'documento_id',
                'cuenta__codigo',
                'cuenta__nombre',
                'cuenta__permite_movimiento',
                'cuenta__exige_grupo',
                'cuenta__exige_contacto',
                'cuenta__exige_base',
                'documento__documento_tipo__nombre'
                
            )
        for movimiento in movimientos:
            if movimiento['cuenta__permite_movimiento'] == False:
                inconsistencias.append({
                    'comprobante_id': movimiento['comprobante_id'],
                    'numero': movimiento['numero'],
                    'cuenta_id': movimiento['cuenta_id'],
                    'documento_id': movimiento['documento_id'],
                    'documento_tipo_nombre': movimiento['documento__documento_tipo__nombre'],
                    'inconsistencia': f'La cuenta {movimiento["cuenta__codigo"]} no permite movimientos y tiene movimientos en el periodo'
                }) 
            if movimiento['cuenta__exige_grupo'] == True:
                if movimiento['grupo_id'] is None:
                    inconsistencias.append({
                        'comprobante_id': movimiento['comprobante_id'],
                        'numero': movimiento['numero'],
                        'cuenta_id': movimiento['cuenta_id'],
                        'documento_id': movimiento['documento_id'],
                        'documento_tipo_nombre': movimiento['documento__documento_tipo__nombre'],                        
                        'inconsistencia': f'La cuenta {movimiento["cuenta__codigo"]} exige grupo y no tiene grupo'
                    })
            if movimiento['cuenta__exige_contacto'] == True:
                if movimiento['contacto_id'] is None:
                    inconsistencias.append({
                        'comprobante_id': movimiento['comprobante_id'],
                        'numero': movimiento['numero'],
                        'cuenta_id': movimiento['cuenta_id'],
                        'documento_id': movimiento['documento_id'],
                        'documento_tipo_nombre': movimiento['documento__documento_tipo__nombre'],                        
                        'inconsistencia': f'La cuenta {movimiento["cuenta__codigo"]} exige contacto y no tiene contacto'
                    })
            if movimiento['cuenta__exige_base'] == True:
                if movimiento['base'] is None or movimiento['base'] == 0:
                    inconsistencias.append({
                        'comprobante_id': movimiento['comprobante_id'],
                        'numero': movimiento['numero'],
                        'cuenta_id': movimiento['cuenta_id'],
                        'documento_id': movimiento['documento_id'],
                        'documento_tipo_nombre': movimiento['documento__documento_tipo__nombre'],                        
                        'inconsistencia': f'La cuenta {movimiento["cuenta__codigo"]} exige base y no tiene base'
                    })           
        return inconsistencias

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
                inconsistencias = self.analizar_inconsistencias(id)    
                return Response({'mensaje': 'Inconsistencia', 'inconsistencias': inconsistencias}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje': 'No existe el periodo'}, status=status.HTTP_400_BAD_REQUEST)                
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                  