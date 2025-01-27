from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.aporte import HumAporte
from humano.models.aporte_contrato import HumAporteContrato
from humano.models.aporte_detalle import HumAporteDetalle
from humano.models.contrato import HumContrato
from general.models.documento_detalle import GenDocumentoDetalle
from humano.serializers.aporte import HumAporteSerializador
from humano.serializers.aporte_contrato import HumAporteContratoSerializador
from humano.serializers.aporte_detalle import HumAporteDetalleSerializador
from datetime import date, timedelta
from django.db.models import Q
import calendar
from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce

class HumAporteViewSet(viewsets.ModelViewSet):
    queryset = HumAporte.objects.all()
    serializer_class = HumAporteSerializador
    permission_classes = [permissions.IsAuthenticated]      

    def perform_create(self, serializer):
        anio = serializer.validated_data.get('anio')
        mes = serializer.validated_data.get('mes')    
        fecha_desde = date(anio, mes, 1)
        ultimo_dia_mes = calendar.monthrange(anio, mes)[1]
        fecha_hasta = date(anio, mes, 30)
        fecha_hasta_periodo = date(anio, mes, ultimo_dia_mes)     
        anio_salud = anio
        mes_salud = mes + 1
        serializer.save(
            fecha_desde=fecha_desde, 
            fecha_hasta=fecha_hasta, 
            fecha_hasta_periodo=fecha_hasta_periodo,
            mes_salud=mes_salud,
            anio_salud=anio_salud)

    def perform_update(self, serializer):
        anio = serializer.validated_data.get('anio')
        mes = serializer.validated_data.get('mes')    
        fecha_desde = date(anio, mes, 1)
        ultimo_dia_mes = calendar.monthrange(anio, mes)[1]
        fecha_hasta = date(anio, mes, 30)
        fecha_hasta_periodo = date(anio, mes, ultimo_dia_mes)     
        anio_salud = anio
        mes_salud = mes + 1
        serializer.save(
            fecha_desde=fecha_desde, 
            fecha_hasta=fecha_hasta, 
            fecha_hasta_periodo=fecha_hasta_periodo,
            mes_salud=mes_salud,
            anio_salud=anio_salud) 
        
    @action(detail=False, methods=["post"], url_path=r'cargar-contrato',)
    def cargar_contrato(self, request):
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                aporte = HumAporte.objects.get(pk=id)                                
                if aporte.estado_generado == False:
                    cantidad = aporte.contratos                    
                    contratos = HumContrato.objects.filter(
                            #grupo_id=programacion.grupo_id                        
                            ).filter(
                                Q(fecha_desde__lte=aporte.fecha_hasta_periodo)                            
                            ).filter(
                                Q(fecha_hasta__gte=aporte.fecha_desde) | Q(contrato_tipo_id=1))
                    #sql_query = str(contratos.query)
                    #print(sql_query)
                    for contrato in contratos:
                        contrato_validar = HumAporteContrato.objects.filter(aporte_id=aporte.id, contrato_id=contrato.id).exists()
                        if not contrato_validar:
                            ingreso = False
                            if contrato.fecha_desde >= aporte.fecha_desde and contrato.fecha_desde <= aporte.fecha_hasta_periodo:
                                ingreso = True                
                            retiro = False
                            if contrato.fecha_hasta <= aporte.fecha_hasta and contrato.fecha_hasta >= aporte.fecha_desde and contrato.contrato_tipo_id != 1:
                                retiro = True
                            data = {
                                'aporte': aporte.id,
                                'contrato': contrato.id,
                                'salario': contrato.salario,
                                'ingreso': ingreso,
                                'retiro': retiro,
                                'error_terminacion': False
                            }
                            ibc = 0
                            fecha_desde = contrato.fecha_desde
                            if fecha_desde < aporte.fecha_desde:
                                fecha_desde = aporte.fecha_desde
                            data['fecha_desde'] = fecha_desde

                            error_terminacion = False    
                            fecha_hasta = contrato.fecha_hasta
                            if contrato.contrato_tipo_id == 1:
                                fecha_hasta = aporte.fecha_hasta
                            else:
                                if contrato.estado_terminado == False:
                                    if contrato.fecha_hasta < aporte.fecha_desde:
                                        fecha_hasta = aporte.fecha_desde
                                        error_terminacion = True
                            if fecha_hasta > aporte.fecha_hasta:
                                fecha_hasta = aporte.fecha_hasta
                            data['fecha_hasta'] = fecha_hasta
                            data['error_terminacion'] = error_terminacion 
                            diferencia = fecha_hasta - fecha_desde
                            dias = diferencia.days + 1
                            if error_terminacion:
                                dias = 0
                            data['dias'] = dias

                            documento_detalle = GenDocumentoDetalle.objects.filter(
                                documento__fecha__gte=fecha_desde,
                                documento__fecha__lte=fecha_hasta,                                                                
                                documento__contrato_id=contrato.id
                            ).aggregate(
                                ibc=Coalesce(Sum('base_cotizacion'), 0, output_field=DecimalField())
                            )
                            ibc = documento_detalle['ibc']
                            data['base_cotizacion'] = ibc
                            aporte_contrato_serializador = HumAporteContratoSerializador(data=data)
                            if aporte_contrato_serializador.is_valid():
                                aporte_contrato_serializador.save()
                                cantidad += 1
                            else:
                                return Response({'validaciones':aporte_contrato_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                    
                    aporte.contratos = cantidad
                    aporte.save()
                    return Response({'contratos': cantidad}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'La programacion ya esta generada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumAporte.DoesNotExist:
            return Response({'mensaje':'El aporte no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 


    @action(detail=False, methods=["post"], url_path=r'generar',)
    def generar(self, request):
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                aporte = HumAporte.objects.get(pk=id)
                if aporte.estado_generado == False and aporte.estado_aprobado == False:
                    aporte_contratos = HumAporteContrato.objects.filter(aporte_id=id)                                           
                    for aporte_contrato in aporte_contratos:                                  
                        data = {
                            'contrato_detalle': aporte_contrato.id                                                
                        }
                        aporte_detalle_serializador = HumAporte(data=data)
                        if aporte_detalle_serializador.is_valid():
                            aporte_detalle = aporte_detalle_serializador.save()                            
                        else:
                            return Response({'validaciones':aporte_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)  


                    aporte.total = 0                    
                    aporte.save()
                    return Response({'total': 0,}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'La programacion ya esta generada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumAporte.DoesNotExist:
            return Response({'mensaje':'La programacion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)               