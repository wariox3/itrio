from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from humano.models.novedad import HumNovedad
from humano.models.contrato import HumContrato
from general.models.configuracion import GenConfiguracion
from humano.serializers.novedad import HumNovedadSerializador, HumNovedadSeleccionarSerializador
from datetime import timedelta
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from humano.filters.novedad import NovedadFilter
from utilidades.excel_exportar import ExcelExportar

class HumNovedadViewSet(viewsets.ModelViewSet):
    queryset = HumNovedad.objects.all()
    serializer_class = HumNovedadSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = NovedadFilter 

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return HumNovedadSerializador
        return self.serializadores[serializador_parametro]

    def get_queryset(self):
        queryset = super().get_queryset()
        serializer_class = self.get_serializer_class()        
        select_related = getattr(serializer_class.Meta, 'select_related_fields', [])
        if select_related:
            queryset = queryset.select_related(*select_related)        
        campos = serializer_class.Meta.fields        
        if campos and campos != '__all__':
            queryset = queryset.only(*campos) 
        return queryset 
    
    def list(self, request, *args, **kwargs):
        if request.query_params.get('excel'):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            exporter = ExcelExportar(serializer.data, nombre_hoja="novedades", nombre_archivo="novedades.xlsx", titulo="Novedades")            
            return exporter.exportar()
        return super().list(request, *args, **kwargs)          

    def liquidar_novedad(self, novedad):
        configuracion = GenConfiguracion.objects.filter(pk=1).values('hum_factor', 'hum_salario_minimo', 'hum_auxilio_transporte')[0]
        contrato = novedad.contrato
        salario = contrato.salario
        diferencia = novedad.fecha_hasta - novedad.fecha_desde
        dias = diferencia.days + 1
        dias_empresa = 0
        dias_entidad = 0
        hora_empresa = 0
        pago_empresa = 0
        hora_entidad = 0
        pago_entidad = 0
        fecha_desde_empresa = None
        fecha_hasta_empresa = None
        fecha_desde_entidad = None
        fecha_hasta_entidad = None
        pago_dia_disfrute = 0
        pago_disfrute = 0
        pago_dia_dinero = 0
        pago_dinero = 0
        total = 0
        dias_acumulados = 0
        hora_minimo = (configuracion['hum_salario_minimo'] / 30) / configuracion['hum_factor']
        dia_minimo = configuracion['hum_salario_minimo'] / 30
        base_cotizacion = salario
        # Incapacidades
        if novedad.novedad_tipo_id in [1, 2]:
            if novedad.novedad_referencia_id:
                try:
                    dias_prorroga = 0
                    novedad_referencia = HumNovedad.objects.get(pk=novedad.novedad_referencia_id)
                    novedad.prorroga = True
                    dias_prorroga = novedad_referencia.dias_acumulados
                except HumNovedad.DoesNotExist:
                    return Response({'mensaje':'La novedad referenciada no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)    
                    
            if novedad.prorroga == True and novedad.novedad_referencia_id is None:
                novedad.prorroga = False

            concepto_empresa = novedad.novedad_tipo.concepto
            concepto_entidad = novedad.novedad_tipo.concepto2
            base_cotizacion = salario
            if contrato.contrato_tipo_id == 5 or contrato.contrato_tipo_id == 6:
                base_cotizacion = configuracion['hum_salario_minimo']
            if novedad.base_cotizacion_propuesto > 0:
                base_cotizacion = novedad.base_cotizacion_propuesto            
            valor_dia = base_cotizacion / 30
            dias_empresa = 0
            dias_entidad = 0
            if novedad.novedad_tipo_id == 1:                
                if dias > 2:
                    if novedad.prorroga:
                        if novedad_referencia.dias_acumulados == 1:
                            dias_empresa = 1
                            dias_entidad = dias - 1        
                        else:
                            dias_empresa = 0
                            dias_entidad = dias
                    else:
                        dias_empresa = 2
                        dias_entidad = dias - 2
                else:
                    if novedad.prorroga:
                        if dias_prorroga < 2:
                            dias_empresa = 1
                            dias_entidad = dias_prorroga + dias - 2
                        else:
                            dias_entidad = dias
                            dias_empresa = 0
                    else:
                        dias_empresa = dias
            else:
                dias_entidad = dias
            # Liquidar empresa
            if dias_empresa > 0:
                porcentaje_empresa = concepto_empresa.porcentaje            
                dia_empresa = (valor_dia * porcentaje_empresa) / 100
                if dia_empresa < dia_minimo:
                    dia_empresa = dia_minimo
                hora_empresa = dia_empresa / configuracion['hum_factor']
                if hora_empresa < hora_minimo:
                    hora_empresa = hora_minimo
                pago_empresa = dias_empresa * dia_empresa
                fecha_desde_empresa = novedad.fecha_desde
                fecha_hasta_empresa = fecha_desde_empresa + timedelta(days=(dias_empresa-1))
                total += pago_empresa

            # Liquidar entidad
            if dias_entidad > 0:
                porcentaje_entidad = concepto_entidad.porcentaje
                dia_entidad = (valor_dia * porcentaje_entidad) / 100
                if dia_entidad < dia_minimo:
                    dia_entidad = dia_minimo
                hora_entidad = dia_entidad / configuracion['hum_factor']
                if hora_entidad < hora_minimo:
                    hora_entidad = hora_minimo
                pago_entidad = dias_entidad * dia_entidad                
                fecha_desde_entidad = novedad.fecha_desde + timedelta(days=(dias_empresa))                
                fecha_hasta_entidad = novedad.fecha_hasta
                total += pago_entidad
        
        # Licencia maternidad o paternidad
        if novedad.novedad_tipo_id == 3:
            dias_entidad = novedad.dias
            base_cotizacion = salario
            if contrato.contrato_tipo_id == 5 or contrato.contrato_tipo_id == 6:
                base_cotizacion = configuracion['hum_salario_minimo']
            if novedad.base_cotizacion_propuesto > 0:
                base_cotizacion = novedad.base_cotizacion_propuesto
            valor_dia = base_cotizacion / 30
            concepto = novedad.novedad_tipo.concepto
            dia_entidad = (valor_dia * concepto.porcentaje) / 100
            hora_entidad = dia_entidad / configuracion['hum_factor']
            pago_entidad = dias_entidad * dia_entidad
            total += pago_entidad
            fecha_desde_entidad = novedad.fecha_desde               
            fecha_hasta_entidad = novedad.fecha_hasta                

        # Licencia luto y remunerada
        if novedad.novedad_tipo_id in [4, 5]:
            valor_dia = base_cotizacion / 30
            hora_empresa = valor_dia / configuracion['hum_factor']
            pago_empresa = dias * valor_dia
            fecha_desde_empresa = novedad.fecha_desde               
            fecha_hasta_empresa = novedad.fecha_hasta    
            total += pago_empresa

        # Vacaciones
        if novedad.novedad_tipo_id == 7:
            pago_dia_disfrute = salario / 30
            pago_disfrute = round(pago_dia_disfrute * novedad.dias_disfrutados_reales)
            pago_dia_dinero = salario / 30
            pago_dinero = round(pago_dia_dinero * novedad.dias_dinero)
            #Esto se hace para pagar en dinero lo proporsional en el periodo en disfrute
            pago_dia_dinero = pago_dinero / novedad.dias_disfrutados_reales
            total += pago_disfrute + pago_dinero
        
        if novedad.prorroga:
            dias_acumulados = novedad_referencia.dias_acumulados + dias
            novedad.dias_acumulados = dias_acumulados
        else:
            novedad.dias_acumulados = dias

        novedad.dias = dias
        novedad.base_cotizacion = base_cotizacion
        novedad.dias_empresa = dias_empresa
        novedad.dias_entidad = dias_entidad
        novedad.hora_empresa = hora_empresa
        novedad.pago_empresa = pago_empresa
        novedad.fecha_desde_empresa = fecha_desde_empresa
        novedad.fecha_hasta_empresa = fecha_hasta_empresa
        novedad.hora_entidad = hora_entidad
        novedad.pago_entidad = pago_entidad
        novedad.fecha_desde_entidad = fecha_desde_entidad
        novedad.fecha_hasta_entidad = fecha_hasta_entidad
        novedad.pago_dia_disfrute = pago_dia_disfrute
        novedad.pago_disfrute = pago_disfrute
        novedad.pago_dia_dinero = pago_dia_dinero
        novedad.pago_dinero = pago_dinero
        novedad.total = total
        novedad.save()

    def validar_rango(self, instance=None):        
        data = self.request.data
        fecha_desde = data.get('fecha_desde')
        fecha_hasta = data.get('fecha_hasta')        
        if instance and not fecha_desde:
            fecha_desde = instance.fecha_desde
        if instance and not fecha_hasta:
            fecha_hasta = instance.fecha_hasta

        if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
            return False, "La fecha desde no puede ser mayor que la fecha hasta"

        if instance:
            contacto_id = instance.contrato.contacto_id
        else:
            contrato = HumContrato.objects.get(pk=data.get('contrato'))
            if contrato:
                contacto_id = contrato.contacto_id
            else:
                return False, "El contrato no existe o no tiene un contacto asociado"

        queryset = HumNovedad.objects.filter(contrato__contacto_id=contacto_id)        
        if instance:
            queryset = queryset.exclude(pk=instance.pk)

        overlapping = queryset.filter(
            fecha_desde__lte=fecha_hasta,
            fecha_hasta__gte=fecha_desde
        ).exists()

        if overlapping:
            return False, "El rango de fechas se cruza con otra novedad existente para este empleado"
        
        return True, None

    def create(self, request, *args, **kwargs):
        valid, message = self.validar_rango()
        if not valid:
            return Response({"mensaje": message},status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        valid, message = self.validar_rango(instance=instance)
        if not valid:
            return Response({"mensaje": message}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        novedad = serializer.save()
        self.liquidar_novedad(novedad)

    def perform_update(self, serializer):
        novedad = serializer.save()
        self.liquidar_novedad(novedad)       

    @action(detail=False, methods=["get"], url_path=r'seleccionar')
    def seleccionar_action(self, request):
        limit = request.query_params.get('limit', 10)
        contrato_id = request.query_params.get('contrato_id', None)
        novedad_tipo_id = request.query_params.get('novedad_tipo_id', None)
        queryset = self.get_queryset()
        if contrato_id:
            queryset = queryset.filter(contrato_id=contrato_id)
        if novedad_tipo_id:
            queryset = queryset.filter(novedad_tipo_id=novedad_tipo_id)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = HumNovedadSeleccionarSerializador(queryset, many=True)        
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path=r'liquidar',)
    def liquidar(self, request):        
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                novedad = HumNovedad.objects.get(pk=id)
                self.liquidar_novedad(novedad)
                return Response({'liquidado': True}, status=status.HTTP_200_OK)                
            except HumNovedad.DoesNotExist:
                return Response({'mensaje':'La novedad no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    