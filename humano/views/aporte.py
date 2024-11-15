from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.aporte import HumAporte
from humano.models.aporte_contrato import HumAporteContrato
from humano.models.contrato import HumContrato
from humano.serializers.aporte import HumAporteSerializador
from humano.serializers.aporte_contrato import HumAporteContratoSerializador
from datetime import date, timedelta
from django.db.models import Q
import calendar

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
                    sql_query = str(contratos.query)
                    #print(sql_query)
                    for contrato in contratos:
                        contrato_validar = HumAporteContrato.objects.filter(aporte_id=aporte.id, contrato_id=contrato.id).exists()
                        if not contrato_validar:
                            data = {
                                'aporte': aporte.id,
                                'contrato': contrato.id,
                                'salario': contrato.salario
                            }
        
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