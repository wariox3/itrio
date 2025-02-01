from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.aporte import HumAporte
from humano.models.aporte_contrato import HumAporteContrato
from humano.models.aporte_detalle import HumAporteDetalle
from humano.models.contrato import HumContrato
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
from datetime import datetime

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
                    cantidad = 0                    
                    contratos = HumContrato.objects.filter(
                            #grupo_id=programacion.grupo_id                        
                            ).filter(
                                Q(fecha_desde__lte=aporte.fecha_hasta_periodo)                            
                            ).filter(
                                Q(fecha_hasta__gte=aporte.fecha_desde) | Q(contrato_tipo_id=1))                    
                    #sql_query = str(contratos.query)
                    #print(sql_query)
                    empleados = contratos.values("contacto_id").distinct().count()
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
                                'ciudad_labora': contrato.ciudad_labora_id,
                                'entidad_salud': contrato.entidad_salud_id,
                                'entidad_pension': contrato.entidad_pension_id,
                                'entidad_caja': contrato.entidad_caja_id,
                                'riesgo': contrato.riesgo_id,
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
                    aporte.empleados = empleados
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
                    base_cotizacion_total = 0
                    aporte_cotizacion_pension = 0
                    aporte_cotizacion_solidaridad_solidaridad = 0
                    aporte_cotizacion_solidaridad_subsistencia = 0
                    aporte_cotizacion_voluntario_pension_afiliado = 0
                    aporte_cotizacion_voluntario_pension_aportante = 0
                    aporte_cotizacion_salud = 0
                    aporte_cotizacion_riesgos = 0
                    aporte_cotizacion_caja = 0
                    aporte_cotizacion_sena = 0
                    aporte_cotizacion_icbf = 0
                    aporte_cotizacion_total = 0                                        
                    lineas = 0
                    aporte_contratos = HumAporteContrato.objects.filter(aporte_id=id)                                           
                    for aporte_contrato in aporte_contratos:                              
                        base_cotizacion = 0
                        dias_contrato = aporte_contrato.dias
                        dias_novedad_contrato = 0
                        documento_detalles = GenDocumentoDetalle.objects.filter(
                            documento__fecha__gte=aporte.fecha_desde,
                            documento__fecha__lte=aporte.fecha_hasta,                                                                
                            documento__contrato_id=aporte_contrato.contrato_id,
                        ).values(
                            'novedad_id', 
                            'novedad__novedad_tipo_id'
                        ).annotate(
                            base_cotizacion=Coalesce(Sum('base_cotizacion'), 0, output_field=DecimalField()), 
                            dias=Sum('dias')
                        )
                        for documento_detalle in documento_detalles:
                            if documento_detalle['novedad_id']:
                                lineas += 1
                                licencia_remunerada = False
                                licencia_maternidad = False
                                incapacidad_general = False
                                base_cotizacion_novedad = documento_detalle['base_cotizacion']
                                dias_novedad = documento_detalle['dias']
                                dias_novedad_contrato += dias_novedad
                                base_cotizacion_total += base_cotizacion_novedad
                                tarifa_pension = 16
                                tarifa_salud = 4
                                tarifa_riesgos = aporte_contrato.riesgo.porcentaje
                                tarifa_caja = 4
                                tarifa_sena = 0
                                tarifa_icbf = 0   

                                if documento_detalle['novedad__novedad_tipo_id'] == 1:
                                    incapacidad_general = True
                                    tarifa_riesgos = 0
                                    tarifa_caja = 0

                                if documento_detalle['novedad__novedad_tipo_id'] == 2:
                                    tarifa_riesgos = 0
                                    tarifa_caja = 0                                    

                                # Licencia maternidad o paternidad
                                if documento_detalle['novedad__novedad_tipo_id'] == 3:
                                    licencia_maternidad = True                                    
                                    tarifa_riesgos = 0
                                    tarifa_caja = 0

                                # Licencia remunerada                                                     
                                if documento_detalle['novedad__novedad_tipo_id'] == 5:
                                    licencia_remunerada = True
                                    tarifa_pension = 12
                                    tarifa_riesgos = 0

                                                                    
                                horas_novedad = dias_novedad * 8   
                                base_cotizacion_pension = base_cotizacion_novedad
                                base_cotizacion_salud = base_cotizacion_novedad
                                base_cotizacion_riesgos = base_cotizacion_novedad
                                base_cotizacion_caja = base_cotizacion_novedad
                                
                                cotizacion_pension = Utilidades.redondear_cien(base_cotizacion_pension * tarifa_pension / 100)
                                cotizacion_solidaridad_solidaridad = Utilidades.redondear_cien(0)
                                cotizacion_solidaridad_subsistencia = Utilidades.redondear_cien(0)
                                cotizacion_voluntario_pension_afiliado = Utilidades.redondear_cien(0)
                                cotizacion_voluntario_pension_aportante = Utilidades.redondear_cien(0)
                                cotizacion_salud = Utilidades.redondear_cien(base_cotizacion_salud * tarifa_salud / 100)
                                cotizacion_riesgos = Utilidades.redondear_cien(base_cotizacion_riesgos * tarifa_riesgos / 100)                    
                                cotizacion_caja = Utilidades.redondear_cien(base_cotizacion_caja * tarifa_caja / 100)
                                cotizacion_sena = Utilidades.redondear_cien(0)
                                cotizacion_icbf = Utilidades.redondear_cien(0)
                                cotizacion_total = cotizacion_pension + cotizacion_salud + cotizacion_riesgos + cotizacion_caja
                                aporte_cotizacion_pension += cotizacion_pension
                                aporte_cotizacion_solidaridad_solidaridad += 0
                                aporte_cotizacion_solidaridad_subsistencia += 0
                                aporte_cotizacion_voluntario_pension_afiliado += 0
                                aporte_cotizacion_voluntario_pension_aportante += 0
                                aporte_cotizacion_salud += cotizacion_salud
                                aporte_cotizacion_riesgos += cotizacion_riesgos
                                aporte_cotizacion_caja += cotizacion_caja   
                                aporte_cotizacion_sena += aporte_cotizacion_sena
                                aporte_cotizacion_icbf += aporte_cotizacion_icbf
                                aporte_cotizacion_total += cotizacion_total                            
                                data = {
                                    'aporte_contrato': aporte_contrato.id,
                                    'ingreso': aporte_contrato.ingreso,
                                    'retiro': aporte_contrato.retiro,
                                    'salario_integral': aporte_contrato.contrato.salario_integral,
                                    'licencia_remunerada': licencia_remunerada,     
                                    'licencia_maternidad': licencia_maternidad, 
                                    'incapacidad_general': incapacidad_general,                    
                                    'horas': horas_novedad,
                                    'dias_pension': dias_novedad,
                                    'dias_salud': dias_novedad,
                                    'dias_riesgos': dias_novedad,
                                    'dias_caja': dias_novedad,
                                    'base_cotizacion_pension': base_cotizacion_pension,
                                    'base_cotizacion_salud': base_cotizacion_salud,
                                    'base_cotizacion_riesgos': base_cotizacion_riesgos,
                                    'base_cotizacion_caja': base_cotizacion_caja,
                                    'tarifa_pension': tarifa_pension,
                                    'tarifa_salud': tarifa_salud,
                                    'tarifa_riesgos': tarifa_riesgos,
                                    'tarifa_caja': tarifa_caja,
                                    'tarifa_sena': tarifa_sena,
                                    'tarifa_icbf': tarifa_icbf,
                                    'cotizacion_pension': cotizacion_pension,
                                    'cotizacion_solidaridad_solidaridad': cotizacion_solidaridad_solidaridad,
                                    'cotizacion_solidaridad_subsistencia': cotizacion_solidaridad_subsistencia,
                                    'cotizacion_voluntario_pension_afiliado': cotizacion_voluntario_pension_afiliado,
                                    'cotizacion_voluntario_pension_aportante': cotizacion_voluntario_pension_aportante,
                                    'cotizacion_salud': cotizacion_salud,
                                    'cotizacion_riesgos': cotizacion_riesgos,
                                    'cotizacion_caja': cotizacion_caja,
                                    'cotizacion_sena': cotizacion_sena,
                                    'cotizacion_icbf': cotizacion_icbf,
                                    'cotizacion_total': cotizacion_total                            
                                }
                                aporte_detalle_serializador = HumAporteDetalleSerializador(data=data)
                                if aporte_detalle_serializador.is_valid():
                                    aporte_detalle_serializador.save()                            
                                else:
                                    return Response({'validaciones':aporte_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)    
                            else:
                                base_cotizacion += documento_detalle['base_cotizacion']  
                                base_cotizacion_total += base_cotizacion                                                                                                      
                        dias_contrato -= dias_novedad_contrato
                        horas = dias_contrato * 8   
                        base_cotizacion_pension = base_cotizacion
                        base_cotizacion_salud = base_cotizacion
                        base_cotizacion_riesgos = base_cotizacion
                        base_cotizacion_caja = base_cotizacion
                        tarifa_pension = 16
                        tarifa_salud = 4
                        tarifa_riesgos = aporte_contrato.riesgo.porcentaje
                        tarifa_caja = 4
                        tarifa_sena = 0
                        tarifa_icbf = 0
                        cotizacion_pension = Utilidades.redondear_cien(base_cotizacion_pension * tarifa_pension / 100)
                        cotizacion_solidaridad_solidaridad = Utilidades.redondear_cien(0)
                        cotizacion_solidaridad_subsistencia = Utilidades.redondear_cien(0)
                        cotizacion_voluntario_pension_afiliado = Utilidades.redondear_cien(0)
                        cotizacion_voluntario_pension_aportante = Utilidades.redondear_cien(0)
                        cotizacion_salud = Utilidades.redondear_cien(base_cotizacion_salud * tarifa_salud / 100)
                        cotizacion_riesgos = Utilidades.redondear_cien(base_cotizacion_riesgos * tarifa_riesgos / 100)                    
                        cotizacion_caja = Utilidades.redondear_cien(base_cotizacion_caja * tarifa_caja / 100)
                        cotizacion_sena = Utilidades.redondear_cien(0)
                        cotizacion_icbf = Utilidades.redondear_cien(0)
                        cotizacion_total = cotizacion_pension + cotizacion_salud + cotizacion_riesgos + cotizacion_caja
                        aporte_cotizacion_pension += cotizacion_pension
                        aporte_cotizacion_solidaridad_solidaridad += 0
                        aporte_cotizacion_solidaridad_subsistencia += 0
                        aporte_cotizacion_voluntario_pension_afiliado += 0
                        aporte_cotizacion_voluntario_pension_aportante += 0
                        aporte_cotizacion_salud += cotizacion_salud
                        aporte_cotizacion_riesgos += cotizacion_riesgos
                        aporte_cotizacion_caja += cotizacion_caja   
                        aporte_cotizacion_sena += aporte_cotizacion_sena
                        aporte_cotizacion_icbf += aporte_cotizacion_icbf
                        aporte_cotizacion_total += cotizacion_total
                        lineas += 1
                        data = {
                            'aporte_contrato': aporte_contrato.id,
                            'ingreso': aporte_contrato.ingreso,
                            'retiro': aporte_contrato.retiro,
                            'salario_integral': aporte_contrato.contrato.salario_integral,                            
                            'horas': horas,
                            'dias_pension': dias_contrato,
                            'dias_salud': dias_contrato,
                            'dias_riesgos': dias_contrato,
                            'dias_caja': dias_contrato,
                            'base_cotizacion_pension': base_cotizacion_pension,
                            'base_cotizacion_salud': base_cotizacion_salud,
                            'base_cotizacion_riesgos': base_cotizacion_riesgos,
                            'base_cotizacion_caja': base_cotizacion_caja,
                            'tarifa_pension': tarifa_pension,
                            'tarifa_salud': tarifa_salud,
                            'tarifa_riesgos': tarifa_riesgos,
                            'tarifa_caja': tarifa_caja,
                            'tarifa_sena': tarifa_sena,
                            'tarifa_icbf': tarifa_icbf,
                            'cotizacion_pension': cotizacion_pension,
                            'cotizacion_solidaridad_solidaridad': cotizacion_solidaridad_solidaridad,
                            'cotizacion_solidaridad_subsistencia': cotizacion_solidaridad_subsistencia,
                            'cotizacion_voluntario_pension_afiliado': cotizacion_voluntario_pension_afiliado,
                            'cotizacion_voluntario_pension_aportante': cotizacion_voluntario_pension_aportante,
                            'cotizacion_salud': cotizacion_salud,
                            'cotizacion_riesgos': cotizacion_riesgos,
                            'cotizacion_caja': cotizacion_caja,
                            'cotizacion_sena': cotizacion_sena,
                            'cotizacion_icbf': cotizacion_icbf,
                            'cotizacion_total': cotizacion_total                            
                        }
                        aporte_detalle_serializador = HumAporteDetalleSerializador(data=data)
                        if aporte_detalle_serializador.is_valid():
                            aporte_detalle_serializador.save()                            
                        else:
                            return Response({'validaciones':aporte_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)
                    aporte.estado_generado = True                                        
                    aporte.cotizacion_pension = aporte_cotizacion_pension
                    aporte.cotizacion_solidaridad_solidaridad = aporte_cotizacion_solidaridad_solidaridad
                    aporte.cotizacion_solidaridad_subsistencia = aporte_cotizacion_solidaridad_subsistencia
                    aporte.cotizacion_voluntario_pension_afiliado = aporte_cotizacion_voluntario_pension_afiliado
                    aporte.cotizacion_voluntario_pension_aportante = aporte_cotizacion_voluntario_pension_aportante
                    aporte.cotizacion_salud = aporte_cotizacion_salud
                    aporte.cotizacion_riesgos = aporte_cotizacion_riesgos
                    aporte.cotizacion_caja = aporte_cotizacion_caja
                    aporte.cotizacion_sena = aporte_cotizacion_sena
                    aporte.cotizacion_icbf = aporte_cotizacion_icbf
                    aporte.cotizacion_total = aporte_cotizacion_total                                                                    
                    aporte.lineas = lineas   
                    aporte.base_cotizacion = base_cotizacion_total           
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
                    aporte.lineas = 0
                    aporte.base_cotizacion = 0
                    aporte.cotizacion_pension = 0
                    aporte.cotizacion_solidaridad_solidaridad = 0
                    aporte.cotizacion_solidaridad_subsistencia = 0
                    aporte.cotizacion_voluntario_pension_afiliado = 0
                    aporte.cotizacion_voluntario_pension_aportante = 0
                    aporte.cotizacion_salud = 0
                    aporte.cotizacion_riesgos = 0
                    aporte.cotizacion_caja = 0
                    aporte.cotizacion_sena = 0
                    aporte.cotizacion_icbf = 0
                    aporte.cotizacion_total = 0                     
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
                    
                    mes_formateado = str(aporte.mes).zfill(2)
                    mes_salud_formateado = str(aporte.mes_salud).zfill(2)
                    periodo_pago = f"{aporte.anio}-{mes_formateado}"
                    periodo_pago_salud = f"{aporte.anio_salud}-{mes_salud_formateado}"
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
                    buffer.write(Utilidades.rellenar('E', 1, " ", "D"))
                    #9	10	228	237	N	Número de Planilla asociada a esta planilla.	Debe dejarse en blanco cuando el tipo de planilla sea E, A, I, M, S, Y, T o X. En este campo se incluirá el número de la planilla del periodo correspondiente cuando el tipo de planilla sea N ó F. Cuando se utilice la planilla U por parte de la UGPP, en este campo se diligenciará el número del título del depósito judicial.                    
                    buffer.write(Utilidades.rellenar('', 10, " ", "D"))
                    #10	10	238	247	A	Fecha de pago Planilla asociada a esta planilla. (AAAA-MM-DD)	Debe dejarse en blanco cuando el tipo de planilla sea E, A, I, M, S, Y, T, o X. En este campo se incluirá la fecha de pago de la planilla del período correspondiente cuando el tipo de planilla sea N ó F. Cuando se utilice la planilla U, la UGPP diligenciará la fecha en que se constituyó el depósito judicial.                    
                    buffer.write(Utilidades.rellenar('', 10, " ", "D"))
                    #11	1	248	248	A	Forma de presentación	El registrado en el campo 10 del archivo tipo 1.                    
                    buffer.write(Utilidades.rellenar(aporte.presentacion, 1, " ", "D"))
                    #12	10	249	258	A	Código de la sucursal del Aportante	El registrado en el campo 5 del archivo tipo 1.                    
                    buffer.write(Utilidades.rellenar(aporte.sucursal.codigo, 10, "0", "I"))
                    #13	40	259	298	A	Nombre de la sucursal	El registrado en el campo 6 del archivo tipo 1.                    
                    buffer.write(Utilidades.rellenar(aporte.sucursal.nombre, 40, " ", "D"))
                    #14	6	299	304	A	Código de la ARL a la cual el aportante se encuentra afiliado	Lo suministra el aportante                    
                    buffer.write(Utilidades.rellenar(aporte.entidad_riesgo.codigo, 6, " ", "D"))
                    #15	7	305	311	A	Periodo de pago para los sistemas diferentes al de salud	Obligatorio. Formato año y mes (aaaa-mm). Lo calcula el Operador de Información.                    
                    buffer.write(Utilidades.rellenar(periodo_pago, 7, " ", "D"))
                    #16	7	312	318	A	Periodo de pago para el sistema de salud	Obligatorio. Formato año y mes (aaaa-mm). Lo suministra el aportante.
                    buffer.write(Utilidades.rellenar(periodo_pago_salud, 7, " ", "D"))
                    #17	10	319	328	N	Número de radicación o de la Planilla Integrada de Liquidación de aportes.	Asignado por el sistema . Debe ser único por operador de información.                    
                    buffer.write(Utilidades.rellenar('', 10, " ", "D"))
                    #18	10	329	338	A	Fecha de pago (aaaa-mm-dd)	Asignado por el sistema a partir de la fecha del día efectivo del pago.                    
                    buffer.write(Utilidades.rellenar('', 10, " ", "D"))
                    #19	5	339	343	N	Número total de empleados	Obligatorio. Se debe validar que sea igual al número de cotizantes únicos incluidos en el detalle del registro tipo 2, exceptuando los que tengan 40 en el campo 5 – Tipo de cotizante.                    
                    buffer.write(Utilidades.rellenar(aporte.empleados, 5, "0", "I"))
                    #20	12	344	355	N	Valor total de la nómina	Obligatorio. Lo suministra el aportante, corresponde a la sumatoria de los IBC para el pago de los aportes de parafiscales de la totalidad de los empleados. Puede ser 0 para independientes                    
                    buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte.base_cotizacion), 12, "0", "I"))
                    #21	2	356	357	N	Tipo de aportante	Obligatorio y debe ser igual al registrado en el campo 30 del archivo tipo 1                    
                    buffer.write(Utilidades.rellenar('01', 2, " ", "D"))
                    #22	2	358	359	N	Código del operador de información	Asignado por el sistema del operador de información.                    
                    buffer.write(Utilidades.rellenar('88', 2, " ", "D"))
                    buffer.write("\n") 
                    secuencia = 1
                    aporte_detalles = HumAporteDetalle.objects.filter(aporte_contrato__aporte_id=id)                   
                    for aporte_detalle in aporte_detalles:
                        ingreso = "X" if aporte_detalle.aporte_contrato.ingreso else " "
                        retiro = "X" if aporte_detalle.aporte_contrato.retiro else " "
                        variacion_permanente_salario = "X" if aporte_detalle.variacion_permanente_salario else " "
                        variacion_transitoria_salario = "X" if aporte_detalle.variacion_transitoria_salario else " "
                        suspension_temporal_contrato = "X" if aporte_detalle.suspension_temporal_contrato else " "
                        incapacidad_general = "X" if aporte_detalle.incapacidad_general else " "
                        licencia_maternidad = "X" if aporte_detalle.licencia_maternidad else " "
                        vacaciones = "X" if aporte_detalle.vacaciones else " "
                        if aporte_detalle.licencia_remunerada:
                            vacaciones = "L"      
                        aporte_voluntario_pension = "X" if aporte_detalle.aporte_voluntario_pension else " "
                        variacion_centro_trabajo = "X" if aporte_detalle.variacion_centro_trabajo else " "
                        salario_integral = "X" if aporte_detalle.salario_integral else "F"
                        #1	2	1	2	N	Tipo de registro	Obligatorio. Debe ser 02.                        
                        buffer.write(Utilidades.rellenar('02', 2, " ", "D"))
                        #2	5	3	7	N	Secuencia	Debe iniciar en 00001 y ser secuencial para el resto de registros. Lo genera el sistema en el caso en que se estén digitando los datos directamente en la web. El aportante debe reportarlo en el caso de que los datos se suban en archivos planos.
                        buffer.write(Utilidades.rellenar(secuencia, 5, "0", "I"))
                        #3	2	8	9	A	Tipo documento el cotizante	Obligatorio. Lo suministra el aportante. Los valores validos son:                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.aporte_contrato.contrato.contacto.identificacion.aporte, 2, " ", "D"))
                        #4	16	10	25	A	Número de identificación del cotizante	Obligatorio. Lo suministra el aportante. El operador de información validará que este campo este compuesto por letras de la A a la Z y los caracteres numéricos del Cero (0) al nueve (9). Sólo es permitido el número de identificación alfanumérico para los siguientes tipos de documentos de identidad: CE.  Cédula de Extranjería PA.  Pasaporte CD.  Carne Diplomático. Para los siguientes tipos de documento deben ser dígitos numéricos: TI.   Tarjeta de Identidad CC. Cédula de ciudadanía  SC.  Salvoconducto de permanencia RC.  Registro Civil                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.aporte_contrato.contrato.contacto.numero_identificacion, 16, " ", "D"))
                        #5	2	26	27	N	Tipo de cotizante	Obligatorio. Lo suministra el aportante. Los valores validos son:                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.aporte_contrato.contrato.tipo_cotizante.codigo, 2, "0", "I"))
                        #6	2	28	29	N	Subtipo de cotizante	Obligatorio. Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.aporte_contrato.contrato.subtipo_cotizante.codigo, 2, "0", "I"))
                        #7	1	30	30	A	Extranjero no obligado a cotizar a pensiones 	Puede ser blanco o X Cuando aplique este campo los únicos tipos de documentos válidos son: CE. Cédula de extranjería PA.  Pasaporte CD.  Carné diplomático Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(' ', 1, "", "I"))
                        #8	1	31	31	A	Colombiano en el exterior	Puede ser blanco o X si aplica.  Este campo es utilizado cuando el tipo de documento es: CC.  Cédula de ciudadanía TI.    Tarjeta de identidad Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(' ', 1, "", "I"))
                        #9	2	32	33	A	Código del departamento de la ubicación laboral	Lo suministra el aportante. El operador de información deberá validar que este código este definido en la relación de la División Política y Administrativa – DIVIPOLA- expedida por el DANE Cuando marque el campo colombiano en el exterior se dejará  en blanco                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.aporte_contrato.ciudad_labora.estado.codigo, 2, "0", "I"))
                        #10	3	34	36	A	Código del Municipio de la ubicación laboral	Lo suministra el aportante. El operador de información deberá validar que este código este definido en la relación de la División Política y Administrativa – DIVIPOLA- expedida por el DANE Cuando marque el campo colombiano en el exterior se dejará en blanco                        
                        buffer.write(aporte_detalle.aporte_contrato.ciudad_labora.codigo[-3:])
                        #11	20	37	56	A	Primer apellido	Obligatorio. Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.aporte_contrato.contrato.contacto.apellido1, 20, " ", "D"))
                        #12	30	57	86	A	Segundo apellido	Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.aporte_contrato.contrato.contacto.apellido2, 30, " ", "D"))
                        #13	20	87	106	A	Primer nombre	Obligatorio. Lo suministra el aportante
                        buffer.write(Utilidades.rellenar(aporte_detalle.aporte_contrato.contrato.contacto.nombre1, 20, " ", "D"))
                        #14	30	107	136	A	Segundo nombre	Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.aporte_contrato.contrato.contacto.nombre2, 30, " ", "D"))
                        #15	1	137	137	A	ING: ingreso	 Puede ser un blanco, R, X o C. Lo suministra el aportante.
                        buffer.write(Utilidades.rellenar(ingreso, 1, " ", "D"))
                        #16	1	138	138	A	RET: retiro	Puede ser un blanco, P, R, X o C. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(retiro, 1, " ", "D"))
                        #17	1	139	139	A	TDE: Traslado desde otra EPS ó EOC	Puede ser un blanco o X. Lo suministra el aportante.
                        buffer.write(Utilidades.rellenar(' ', 1, " ", "D"))
                        #18	1	140	140	A	TAE: Traslado a otra EPS ó EOC	Puede ser un blanco o X. Lo suministra el aportante.                    
                        buffer.write(Utilidades.rellenar(' ', 1, " ", "D"))
                        #19	1	141	141	A	TDP: Traslado desde otra Administradora de Pensiones	Puede ser un blanco o X. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(' ', 1, " ", "D"))
                        #20	1	142	142	A	TAP: Traslado a otra  administradora de pensiones	Puede ser un blanco o X. Lo suministra el aportante.                
                        buffer.write(Utilidades.rellenar(' ', 1, " ", "D"))
                        #21	1	143	143	A	VSP: Variación permantente de salario	Puede ser un blanco o X. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(variacion_permanente_salario, 1, " ", "D"))
                        #22	1	144	144	A	Correcciones	Puede ser un blanco, A o C. Lo suministra el aportante
                        buffer.write(Utilidades.rellenar(' ', 1, " ", "D"))
                        #23	1	145	145	A	VST: Variación transitoria del salario	Puede ser un blanco o X. Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar(variacion_transitoria_salario, 1, " ", "D"))
                        #24	1	146	146	A	SLN: suspensión temporal del contrato de trabajo o licencia no remunerada o comisión de servicios	Puede ser un blanco, X o C. Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar(suspension_temporal_contrato, 1, " ", "D"))
                        #25	1	147	147	A	IGE: Incapacidad Temporal por Enfermedad General	Puede ser un blanco o X. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(incapacidad_general, 1, " ", "D"))
                        #26	1	148	148	A	LMA: Licencia de Maternidad  o de Paternidad	Puede ser un blanco o X. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(licencia_maternidad, 1, " ", "D"))
                        #27	1	149	149	A	VAC- LR: Vacaciones, Licencia Remunerada 	Puede ser: X:   Vacaciones L:    Licencia remunerada Blanco: Cuando no aplique esta novedad.                        
                        buffer.write(Utilidades.rellenar(vacaciones, 1, " ", "D"))
                        #28	1	150	150	A	AVP: Aporte Voluntario	Puede ser un blanco o X. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(aporte_voluntario_pension, 1, " ", "D"))
                        #29	1	151	151	A	VCT: Variación centros de trabajo	Puede ser un blanco o X. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(variacion_centro_trabajo, 1, " ", "D"))
                        #30	2	152	153	N	IRL:Dias de  Incapacidad por accidente de trabajo o enfermedad laboral	Puede ser cero o el número de días (entre 01 y 30). Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.dias_incapacidad_laboral, 2, "0", "I"))
                        #31	6	154	159	A	Código de la Administradora de Fondo de Pensiones a la cual pertenece el afiliado	Es un campo obligatorio y solo se permite blanco, si el tipo de cotizante o el subtipo de cotizante no es obligado a aportar al Sistema General de Pensiones. Se debe utilizar un código válido y este lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.aporte_contrato.entidad_pension.codigo, 6, " ", "D"))
                        #32	6	160	165	A	Código de la Administradora de Fondo de Pensiones a la cual se tralada el afiliado	Obligatorio si la novedad es traslado a otra administradora de fondo de pensiones. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(" ", 6, " ", "D"))
                        #33	6	166	171	A	Código EPS ó EOC a la cual pertenece el afiliado	Es un campo obligatorio. Se debe utilizar un código válido y éste lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.aporte_contrato.entidad_salud.codigo, 6, " ", "D"))
                        #34	6	172	177	A	Código EPS ó EOC a la cual se traslada el afiliado	Obligatorio si en el campo 18 del registro tipo 2 se marca X. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(" ", 6, " ", "D"))
                        #35	6	178	183	A	Código CCF a la que pertenece el afiliado	Obligatorio y solo se permite blanco, si el tipo de cotizante no es obligado a aportar a CCF. Se debe utilizar un código válido y este lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.aporte_contrato.entidad_caja.codigo, 6, " ", "D"))
                        #36	2	184	185	N	Número de días cotizados a pensión	Obligatorio y debe permitir valores entre 0 y 30. Solo se permite 0, si el tipo de cotizante o subtipo de cotizante no está obligado a aportar pensiones. Si es menor que 30 debe haber marcado una novedad de ingreso o retiro. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.dias_pension, 2, "0", "I"))
                        #37	2	186	187	N	Número de días cotizados a salud	Obligatorio y debe permitir valores entre 0 y 30. Si es menor que 30 debe haber marcado  una  novedad  de ingreso o retiro. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.dias_salud, 2, "0", "I"))
                        #38	2	188	189	N	Número de días cotizados a Riesgos Laborales	Obligatorio y debe permitir valores entre 0 y 30. Solo se permite 0, si el tipo de cotizante no está obligado a aportar al Sistema General de Riesgos Laborales, o si en los campos 25, 26, 27, del registro tipo 2 se ha marcado X o el campo 30 del registro tipo 2 es mayor que 0. Si es menor que 30 debe haber marcado la novedad correspondiente. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.dias_riesgos, 2, "0", "I"))
                        #39	2	190	191	N	Número de días cotizados a Caja de Compensación Familiar	Obligatorio y debe permitir valores entre 0 y 30. Solo se permite 0, si el tipo de cotizante no está obligado a aportar a Cajas de Compensación Familiar  Si es menor que 30 debe haber marcado la novedad correspondiente. Lo suministra el aportante.
                        buffer.write(Utilidades.rellenar(aporte_detalle.dias_caja, 2, "0", "I"))
                        #40	9	192	200	N	Salario básico 	Obligatorio, sin comas ni puntos. No puede ser menor cero. Puede ser menor que 1 smlmv. Lo suministra el aportante Este valor debe ser reportado sin centavos                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.aporte_contrato.salario), 9, "0", "I"))
                        #41	1	201	201	A	Salario Integral	Se debe indicar con una X si el salario es integral o blanco si no lo es. Es responsabilidad del aportante suministrar esta información.                        
                        buffer.write(Utilidades.rellenar(salario_integral, 1, " ", "D"))
                        #42	9	202	210	N	IBC Pensión	Obligatorio. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.base_cotizacion_pension), 9, "0", "I"))
                        #43	9	211	219	N	IBC Salud	Obligatorio. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.base_cotizacion_salud), 9, "0", "I"))
                        #44	9	220	228	N	IBC Riesgos Laborales	Obligatorio. Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.base_cotizacion_riesgos), 9, "0", "I"))
                        #45	9	229	237	N	IBC CCF	 Es un campo obligatorio para los tipos de cotizante 1, 2, 18,22, 30, 51 y 55.  Lo suministra el aportante.  Para el caso del tipo de cotizante 31 no es obligatorio cuando la cooperativa o precooperativa de trabajo asociado este exceptuada por el Ministerio del Trabajo.                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.base_cotizacion_caja), 9, "0", "I"))
                        #46	7	238	244	N	Tarifa de aportes pensiones	Lo suministra el aportante y la valida el Operador de Información de acuerdo con las tarifas vigentes en el periodo a liquidar                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.tarifa_pension / 100, 7, "0", "D"))
                        #47	9	245	253	N	Cotización obligatoria a Pensiones	Obligatorio. Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.cotizacion_pension), 9, "0", "I"))
                        #48	9	254	262	N	Aporte voluntario del afiliado al Fondo de Pensiones Obligatorias	Lo suministra el aportante. Solo aplica para las Administradoras de Pensiones del Régimen de ahorro individual                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.cotizacion_voluntario_pension_afiliado), 9, "0", "I"))
                        #49	9	263	271	N	Aporte voluntario del aportante al fondo de pensiones obligatoria. 	Lo suministra el aportante. Solo aplica para las Administradoras de Pensiones del Régimen de ahorro individual                                                
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.cotizacion_voluntario_pension_aportante), 9, "0", "I"))
                        #50	9	272	280	N	Total cotización sistema general de pensiones	Lo calcula el sistema. Sumatoria de los campos 47, 48 y 49 del registro tipo 2.                        
                        total_pension = aporte_detalle.cotizacion_pension + aporte_detalle.cotizacion_voluntario_pension_afiliado + aporte_detalle.cotizacion_voluntario_pension_aportante
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(total_pension), 9, "0", "I"))
                        #51	9	281	289	N	Aportes a Fondo de Solidaridad  Pensional- Subcuenta de solidaridad	Lo suministra el aportante cuando aplique                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.cotizacion_solidaridad_solidaridad), 9, "0", "I"))
                        #52	9	290	298	N	Aportes a Fondo de Solidad Pensional- Subcuenta de subsistencia	Lo suministra el aportante cuando aplique                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.cotizacion_solidaridad_subsistencia), 9, "0", "I"))
                        #53	9	299	307	N	Valor no retenido por aportes voluntarios	Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar("", 9, "0", "I"))
                        #54	7	308	314	N	Tarifa de aportes de salud	Lo suministra el aportante y la valida el Operador de Información de acuerdo con las tarifas vigentes en el periodo a liquidar                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.tarifa_salud / 100, 7, "0", "D"))
                        #55	9	315	323	N	Cotización Obligatoria a salud	Obligatorio. Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.cotizacion_salud), 9, "0", "I"))
                        #56	9	324	332	N	Valor de la UPC adicional	Debe corresponder al valor reportado en el campo 11 del archivo “información de la Base de Datos Única de Afiliados – BDUA con destino a los operadores de información”
                        #fputs($ar, FuncionesController::RellenarNr($arAporteDetalle->getValorUpcAdicional(), "0", 9, "I"));
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.upc_adicional), 9, "0", "I"))
                        #57	15	333	347	A	N° autorización de la incapacidad por enfermedad general	Debe reportarse en blanco                        
                        buffer.write(Utilidades.rellenar("", 15, " ", "D"))
                        #58	9	348	356	N	Valor de incapacidad por enfermedad general	Debe reportarse en blanco                        
                        buffer.write(Utilidades.rellenar("", 9, "0", "I"))
                        #59	15	357	371	A	N° autorización de la licencia de maternidad o paternidad	Debe reportarse en blanco                        
                        buffer.write(Utilidades.rellenar("", 15, " ", "D"))
                        #60	9	372	380	N	Valor de la licencia de maternidad	Debe reportarse en cero                        
                        buffer.write(Utilidades.rellenar("", 9, "0", "I"))
                        #61	9	381	389	N	Tarifa de aportes a Riesgos Laborales	Lo suministra el aportante y la valida el Operador de Información de acuerdo con las tarifas vigentes en el periodo a liquidar                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.tarifa_riesgos / 100, 9, "0", "D"))
                        #62	9	390	398	N	Centro de Trabajo CT	Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar("", 9, "0", "I"))
                        #63	9	399	407	N	Cotización obligatoria al Sistema General de Riesgos Laborales	Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.cotizacion_riesgos), 9, "0", "I"))
                        #64	7	408	414	N	Tarifa de aportes CCF	Lo suministra el aportante y la valida el Operador de Información de acuerdo con las tarifas vigentes en el periodo a liquidar                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.tarifa_caja / 100, 7, "0", "D"))
                        #65	9	415	423	N	Valor aporte CCF	Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.cotizacion_caja), 9, "0", "I"))
                        #66	7	424	430	N	Tarifa de aportes SENA	Lo suministra el aportante                        
                        buffer.write("0.00000" if (aporte_detalle.tarifa_sena / 100) == 0 else Utilidades.rellenar(aporte_detalle.tarifa_sena / 100, 7, 0, "D"))
                        #67	9	431	439	N	Valor aportes SENA	Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.cotizacion_sena), 9, "0", "I"))
                        #68	7	440	446	N	Tarifa aportes ICBF	Lo suministra el aportante                        
                        buffer.write("0.00000" if (aporte_detalle.tarifa_icbf / 100) == 0 else Utilidades.rellenar(aporte_detalle.tarifa_icbf / 100, 7, 0, "D"))
                        #69	9	447	455	N	Valor aporte ICBF	Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.cotizacion_icbf), 9, "0", "I"))
                        #70	7	456	462	N	Tarifa aportes ESAP	Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar("0.00000", 7, "0", "D"))
                        #71	9	463	471	N	Valor aporte ESAP	Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar("", 9, "0", "I"))
                        #72	7	472	478	N	Tarifa aportes MEN	Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar("0.00000", 7, "0", "D"))
                        #73	9	479	487	N	Valor aporte MEN	Lo suministra el aportante                        
                        buffer.write(Utilidades.rellenar("", 9, "0", "I"))
                        #74	2	488	489	A	Tipo de documento del cotizante principal	Corresponde al tipo de documento del cotizante Principal que corresponde a: CC.  Cédula de ciudadanía CE.  Cédula de extranjería TI.    Tarjeta de identidad PA.  Pasaporte CD.  Carné diplomático SC.  Salvoconducto de permanencia Lo suministra el aportante Solo debe ser reportado cuando se reporte un cotizante 40.                        
                        buffer.write(Utilidades.rellenar("", 2, " ", "D"))
                        #75	16	490	505	A	Número de identificación del cotizante principal	Lo suministra el aportante Solo debe ser reportado cuando se reporte un cotizante 40. El operador de información validará que este campo este compuesto por letras de la A a la Z y los caracteres numéricos del Cero (0) al nueve (9). Sólo es permitido el número de identificación alfanumérico para los siguientes tipos de documentos de identidad: CE.  Cédula de Extranjería PA.  Pasaporte CD.  Carne Diplomático   Para los siguientes tipos de documento deben ser dígitos numéricos: TI.   Tarjeta de Identidad CC. Cédula de ciudadanía  SC.  Salvoconducto de permanencia                        
                        buffer.write(Utilidades.rellenar("", 16, " ", "D"))
                        #76	1	506	506	A	Cotizante exonerado de pago de aporte salud, SENA e ICBF - Ley 1607 de 2012 	Obligatorio.  Lo suministra el aportante. S = Si  N = No Cuando el valor del campo 43 – IBC Salud sea superior a 10 SMLMV este campo debe ser N Obligatorio.  Lo suministra el aportante. S = Si  N = No   Cuando personas naturales empleen dos o más trabajadores y el valor del campo 43 – IBC Salud sea superior a 10 SMLMV este campo debe ser N                        
                        buffer.write(Utilidades.rellenar("S", 1, " ", "D"))
                        #77	6	507	512	A	Código de la Administradora de Riesgos Laborales a la cual pertenece el afiliado	Lo suministra el aportante. Para el caso de cotizantes diferente al cotizante 3- independiente, se debe registrar el valor ingresado en el Campo 14 del registro Tipo 1 del archivo Tipo 2. Se deja en blanco cuando no sea obligatorio para el cotizante estar afiliado a una Administradora de Riesgos Laborales.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.aporte_contrato.aporte.entidad_riesgo.codigo, 6, " ", "D"))
                        #78	1	513	513	A	Clase de riesgo en la que se encuentra el afiliado	Lo suministra el aportante. 1. Clase de Riesgo I 2. Clase de Riesgo II 3. Clase de Riesgo III 4. Clase de Riesgo IV  5. Clase de Riesgo V  La clase de riesgo de acuerdo a la actividad económica establecida en el Decreto 1607 de 2002 o la norma que lo sustituya o modifique                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.aporte_contrato.riesgo.id, 1, " ", "D"))
                        #79	1	514	514	A	Indicador tarifa especial pensiones 	Lo suministra el aportante y es: Blanco  Tarifa normal 1. Actividades de alto riesgo 2. Senadores 3. CTI 4. Aviadores                        
                        buffer.write(Utilidades.rellenar(" ", 1, " ", "D"))
                        #80	10	515	524	A	Fecha de ingreso Formato (AAAA-MM- DD). 	Es obligatorio cuando se reporte la novedad de ingreso. Lo suministra el aportante. Debe reportarse una fecha valida siempre y cuando la novedad se presente en el periodo que se esté liquidando  Cuando no se reporte la novedad el campo se dejará en blanco.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.fecha_ingreso, 10, " ", "D"))
                        #81	10	525	534	A	Fecha de retiro. Formato (AAAA-MM- DD).	Es obligatorio cuando se reporte la novedad de retiro.  Lo suministra el aportante. Debe reportarse una fecha valida siempre y cuando la novedad se presente en el periodo que se esté liquidando  Cuando no se reporte la novedad el campo se dejará en blanco.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.fecha_retiro, 10, " ", "D"))
                        #82	10	535	544	A	Fecha Inicio  VSP Formato (AAAA-MM- DD).	Es obligatorio cuando se reporte la novedad de VSP.  Lo suministra el aportante Debe reportarse una fecha valida siempre y cuando la novedad se presente en el periodo que se esté liquidando  Cuando no se reporte la novedad el campo se dejará en blanco                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.fecha_inicio_variacion_permanente_salario, 10, " ", "D"))
                        #83	10	545	554	A	Fecha Inicio SLN Formato (AAAA-MM- DD). 	Es obligatorio cuando se reporte la novedad de SLN. Lo suministra el aportante.   Debe reportarse una fecha valida siempre y cuando la novedad se presente en el periodo que se esté liquidando  Cuando no se reporte la novedad el campo se dejará en blanco.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.fecha_inicio_suspension_temporal_contrato, 10, " ", "D"))
                        #84	10	555	564	A	Fecha fin SLN Formato (AAAA-MM- DD). 	Es obligatorio cuando se reporte la novedad de SLN. Lo suministra el aportante.  Debe reportarse una fecha valida siempre y cuando la novedad se presente en el periodo que se esté liquidando Cuando no se reporte la novedad el campo se dejará en blanco.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.fecha_fin_suspension_temporal_contrato, 10, " ", "D"))
                        #85	10	565	574	A	Fecha inicio  IGE Formato (AAAA-MM- DD).	Es obligatorio cuando se reporte la novedad de IGE.  Lo suministra el aportante. Debe reportarse una fecha valida siempre y cuando la novedad se presente en el periodo que se esté liquidando  Cuando no se reporte la novedad el campo se dejará en blanco                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.fecha_inicio_incapacidad_general, 10, " ", "D"))
                        #86	10	575	584	A	Fecha fin IGE. Formato (AAAA-MM- DD) 	Es obligatorio cuando se reporte la novedad de IGE. Lo suministra el aportante.  Debe reportarse una fecha valida siempre y cuando la novedad se presente en el periodo que se esté liquidando  Cuando no se reporte la novedad el campo se dejará en blanco                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.fecha_fin_incapacidad_general, 10, " ", "D"))
                        #87	10	585	594	A	Fecha inicio LMA Formato (AAAA-MM- DD). 	Es obligatorio cuando se reporte la novedad de LMA.  Lo suministra el aportante. Debe reportarse una fecha valida siempre y cuando la novedad se presente en el periodo que se esté liquidando  Cuando no se reporte la novedad el campo se dejará en blanco.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.fecha_inicio_licencia_maternidad, 10, " ", "D"))
                        #88	10	595	604	A	Fecha fin LMA Formato (AAAA-MM- DD) 	Es obligatorio cuando se reporte la novedad de LMA.  Lo suministra el aportante. Debe reportarse una fecha valida siempre y cuando la novedad se presente en el periodo que se esté liquidando  Cuando no se reporte la novedad el campo se dejará en blanco.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.fecha_fin_licencia_maternidad, 10, " ", "D"))
                        #89	10	605	614	A	Fecha inicio VAC - LR Formato (AAAA-MM- DD). 	Es obligatorio cuando se reporte la novedad VAC - LR. Debe reportarse una fecha valida siempre y cuando la novedad se presente en el periodo que se esté liquidando  Cuando no se reporte la novedad el campo se dejará en blanco.
                        buffer.write(Utilidades.rellenar(aporte_detalle.fecha_inicio_vacaciones, 10, " ", "D"))
                        #90	10	615	624	A	Fecha fin VAC - LR Formato (AAAA-MM- DD). 	Es obligatorio cuando se reporte la novedad VAC - LR. Debe reportarse una fecha valida siempre y cuando la novedad se presente en el periodo que se esté liquidando  Cuando no se reporte la novedad el campo se dejará en blanco.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.fecha_fin_vacaciones, 10, " ", "D"))
                        #91	10	625	634	A	Fecha inicio VCT Formato (AAAA-MM- DD). 	Es obligatorio cuando se reporte la novedad VCT.  Lo suministra el aportante. Debe reportarse una fecha valida siempre y cuando la novedad se presente en el periodo que se esté liquidando  Cuando no se reporte la novedad el campo se dejará en blanco                        
                        buffer.write(Utilidades.rellenar(" ", 10, " ", "D"))
                        #92	10	635	644	A	Fecha fin  VCT Formato (AAAA-MM- DD). 	Cuando no se reporte la novedad el campo se dejará en blanco.                        
                        buffer.write(Utilidades.rellenar(" ", 10, " ", "D"))
                        #93	10	645	654	A	Fecha inicio IRL Formato (AAAA-MM- DD). 	Es obligatorio cuando se reporte la novedad IRL. Debe reportarse una fecha valida siempre y cuando la novedad se presente en el periodo que se esté liquidando  Cuando no se reporte la novedad el campo se dejará en blanco.
                        buffer.write(Utilidades.rellenar(aporte_detalle.fecha_inicio_incapacidad_laboral, 10, " ", "D"))
                        #94	10	655	664	A	Fecha fin  IRL Formato (AAAA-MM- DD). 	Es obligatorio cuando se reporte la novedad IRL. Debe reportarse una fecha valida siempre y cuando la novedad se presente en el periodo que se esté liquidando  Cuando no se reporte la novedad el campo se dejará en blanco                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.fecha_fin_incapacidad_laboral, 10, " ", "D"))
                        #95	9	665	673	N	IBC otros parafiscales diferentes a CCF	Es un campo obligatorio para los tipos de cotizante 1, 18, 20, 22, 30, 31, y 55.   Lo suministra el aportante.                        
                        buffer.write(Utilidades.rellenar(Utilidades.obtener_valor_formateado(aporte_detalle.base_cotizacion_otros_parafiscales), 9, "0", "D"))
                        #96	3	674	676	N	Número de horas laboradas 	Es un campo obligatorio para los tipos de cotizante 1, 2, 18, 22, 30, 51 y 55.  Lo suministra el aportante.  Para el caso del tipo de cotizante 31 no es obligatorio cuando la cooperativa o precooperativa de trabajo asociado este exceptuada por el Ministerio del Trabajo.                        
                        buffer.write(Utilidades.rellenar(aporte_detalle.horas, 3, "0", "I"))
                        #97	10	???	???	A	Fecha
                        buffer.write(Utilidades.rellenar(" ", 10, " ", "D"))                        
                        #97	7	687	693	A	Actividad económica para el sistema general de riesgos laborales
                        buffer.write(Utilidades.rellenar("1620101", 7, "0", "D"))                                                
                        secuencia += 1
                        buffer.write("\n") 
                    buffer.seek(0)          
                    contenido_bytes = buffer.getvalue().encode("ISO-8859-15")          
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    response = HttpResponse(contenido_bytes, content_type='text/csv; charset=ISO-8859-15')
                    response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                    response['Content-Disposition'] = f'attachment; filename="pila{timestamp}.txt"'
                    return response
                else:
                    return Response({'mensaje':'El aporte aun no esta generado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumAporte.DoesNotExist:
            return Response({'mensaje':'El aporte no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                           