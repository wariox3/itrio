from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.aporte import HumAporte
from humano.models.aporte_contrato import HumAporteContrato
from humano.models.aporte_detalle import HumAporteDetalle
from humano.models.contrato import HumContrato
from general.models.configuracion import GenConfiguracion
from general.models.empresa import GenEmpresa
from general.models.documento_detalle import GenDocumentoDetalle
from humano.serializers.aporte import HumAporteSerializador
from humano.serializers.aporte_contrato import HumAporteContratoSerializador
from humano.serializers.aporte_detalle import HumAporteDetalleSerializador
from datetime import date, timedelta
from django.db.models import Sum, Q, Value, DecimalField
from django.db.models.functions import Coalesce
from utilidades.utilidades import Utilidades
from django.http import HttpResponse
import calendar
import io


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
                            'aporte_contrato': aporte_contrato.id,
                            'ingreso': False,
                            'retiro': False                                              
                        }
                        aporte_detalle_serializador = HumAporteDetalleSerializador(data=data)
                        if aporte_detalle_serializador.is_valid():
                            aporte_detalle_serializador.save()                            
                        else:
                            return Response({'validaciones':aporte_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)
                    aporte.estado_generado = True
                    aporte.total = 0                    
                    aporte.save()
                    return Response({'total': 0,}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'El aporte ya esta generado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumAporte.DoesNotExist:
            return Response({'mensaje':'El aporte no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=False, methods=["post"], url_path=r'desgenerar',)
    def desgenerar(self, request):             
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                aporte = HumAporte.objects.get(pk=id)
                if aporte.estado_aprobado == False and aporte.estado_generado == True:
                    aporte_contratos = HumAporteContrato.objects.filter(aporte_id=id)
                    for aporte_contrato in aporte_contratos:
                        aporte_detalles = HumAporteDetalle.objects.filter(aporte_contrato_id=aporte_contrato.id)
                        aporte_detalles.delete()
                    aporte.estado_generado = False
                    aporte.total = 0                    
                    aporte.save()
                    return Response({'mensaje': 'Aporte desgenerado'}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'El aporte ya esta aprobado o no esta generado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumAporte.DoesNotExist:
            return Response({'mensaje':'El aporte no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)    

    @action(detail=False, methods=["post"], url_path=r'plano-operador',)
    def plano_operador(self, request):             
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                aporte = HumAporte.objects.get(pk=id)
                if aporte.estado_generado == True:
                    
                    empresa = GenEmpresa.objects.filter(pk=1).values('nombre_corto', 'numero_identificacion', 'digito_verificacion').first()
                    buffer = io.StringIO()
                    #1	2	1	2	N	Tipo de registro	Obligatorio. Debe ser 01
                    buffer.write("01")
                    #2	1	3	3	N	Modalidad de la Planilla	Obligatorio. Lo genera autómaticamente el Operador de Información.
                    buffer.write("1")
                    #3	4	4	7	N	Secuencia	Obligatorio. Verificación de la secuencia ascendente. Para cada aportante inicia en 0001. Lo genera el sistema en el caso en que se estén digitando los datos directamente en la web. El aportante debe reportarlo en el caso de que los datos se suban en archivos planos.
                    buffer.write("0001")
                    #4	200	8	207	A	Nombre o razón social del aportante	El registrado en el campo 1 del archivo tipo 1
                    buffer.write(Utilidades.rellenar(empresa['nombre_corto'], 200, " ", "D"))
                    #5	2	208	209	A	Tipo documento del aportante	El registrado en el campo 2 del archivo tipo 1
                    buffer.write("NI")
                    #6	16	210	225	A	Número de identificación del aportante	El registrado en el campo 3 del archivo tipo 1
                    buffer.write(Utilidades.rellenar(empresa['numero_identificacion'], 16, " ", "D"))                    
                    #7	1	226	226	N	Dígito de verificación aportante	El registrado en el campo 4 del archivo tipo 1
                    buffer.write(Utilidades.rellenar(empresa['digito_verificacion'], 1, " ", "D"))                                        
                    #8	1	227	227	A	Tipo de Planilla	Obligatorio lo suministra el aportante
                    #fputs($ar, FuncionesController::RellenarNr("E", " ", 1, "D"));
                    #9	10	228	237	N	Número de Planilla asociada a esta planilla.	Debe dejarse en blanco cuando el tipo de planilla sea E, A, I, M, S, Y, T o X. En este campo se incluirá el número de la planilla del periodo correspondiente cuando el tipo de planilla sea N ó F. Cuando se utilice la planilla U por parte de la UGPP, en este campo se diligenciará el número del título del depósito judicial.
                    #fputs($ar, FuncionesController::RellenarNr("", " ", 10, "D"));
                    #10	10	238	247	A	Fecha de pago Planilla asociada a esta planilla. (AAAA-MM-DD)	Debe dejarse en blanco cuando el tipo de planilla sea E, A, I, M, S, Y, T, o X. En este campo se incluirá la fecha de pago de la planilla del período correspondiente cuando el tipo de planilla sea N ó F. Cuando se utilice la planilla U, la UGPP diligenciará la fecha en que se constituyó el depósito judicial.
                    #fputs($ar, FuncionesController::RellenarNr("", " ", 10, "D"));
                    #11	1	248	248	A	Forma de presentación	El registrado en el campo 10 del archivo tipo 1.
                    #fputs($ar, FuncionesController::RellenarNr($arAporte->getFormaPresentacion(), " ", 1, "D"));
                    #12	10	249	258	A	Código de la sucursal del Aportante	El registrado en el campo 5 del archivo tipo 1.
                    #fputs($ar, FuncionesController::RellenarNr($codigoSucursal, " ", 10, "D"));
                    #13	40	259	298	A	Nombre de la sucursal	El registrado en el campo 6 del archivo tipo 1.
                    #fputs($ar, FuncionesController::RellenarNr($sucursal, " ", 40, "D"));
                    #14	6	299	304	A	Código de la ARL a la cual el aportante se encuentra afiliado	Lo suministra el aportante
                    #fputs($ar, FuncionesController::RellenarNr($arEntidadRiesgos->getCodigoInterface(), " ", 6, "D"));
                    #15	7	305	311	A	Periodo de pago para los sistemas diferentes al de salud	Obligatorio. Formato año y mes (aaaa-mm). Lo calcula el Operador de Información.
                    #fputs($ar, FuncionesController::RellenarNr($periodoPagoDiferenteSalud, " ", 7, "D"));
                    #16	7	312	318	A	Periodo de pago para el sistema de salud	Obligatorio. Formato año y mes (aaaa-mm). Lo suministra el aportante.
                    #fputs($ar, FuncionesController::RellenarNr($periodoPagoSalud, " ", 7, "D"));
                    #17	10	319	328	N	Número de radicación o de la Planilla Integrada de Liquidación de aportes.	Asignado por el sistema . Debe ser único por operador de información.
                    #fputs($ar, FuncionesController::RellenarNr("", " ", 10, "D"));
                    #18	10	329	338	A	Fecha de pago (aaaa-mm-dd)	Asignado por el sistema a partir de la fecha del día efectivo del pago.
                    #fputs($ar, FuncionesController::RellenarNr("", " ", 10, "D"));
                    #19	5	339	343	N	Número total de empleados	Obligatorio. Se debe validar que sea igual al número de cotizantes únicos incluidos en el detalle del registro tipo 2, exceptuando los que tengan 40 en el campo 5 – Tipo de cotizante.
                    #fputs($ar, FuncionesController::RellenarNr($arAporte->getCantidadEmpleados(), "0", 5, "I"));
                    #20	12	344	355	N	Valor total de la nómina	Obligatorio. Lo suministra el aportante, corresponde a la sumatoria de los IBC para el pago de los aportes de parafiscales de la totalidad de los empleados. Puede ser 0 para independientes
                    #fputs($ar, FuncionesController::RellenarNr($arAporte->getVrIngresoBaseCotizacion(), "0", 12, "I"));
                    #21	2	356	357	N	Tipo de aportante	Obligatorio y debe ser igual al registrado en el campo 30 del archivo tipo 1
                    #fputs($ar, FuncionesController::RellenarNr("01", " ", 2, "D"));
                    #22	2	358	359	N	Código del operador de información	Asignado por el sistema del operador de información.
                    #fputs($ar, FuncionesController::RellenarNr("88", " ", 2, "D"));
                    buffer.write("\n") 
                    aporte_detalles = HumAporteDetalle.objects.filter(aporte_contrato__aporte_id=id)                   
                    for aporte_detalle in aporte_detalles:
                        buffer.write(f"02\n")            
                    buffer.seek(0)
                    
                    response = HttpResponse(buffer, content_type='text/plain')
                    response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                    response['Content-Disposition'] = f'attachment; filename="plano_operador_{id}.txt"'
                    return response
                else:
                    return Response({'mensaje':'El aporte aun no esta generado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumAporte.DoesNotExist:
            return Response({'mensaje':'El aporte no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                           