from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from humano.models.novedad import HumNovedad
from general.models.configuracion import GenConfiguracion
from humano.serializers.novedad import HumNovedadSerializador

class HumNovedadViewSet(viewsets.ModelViewSet):
    queryset = HumNovedad.objects.all()
    serializer_class = HumNovedadSerializador
    permission_classes = [permissions.IsAuthenticated]

    def liquidar_novedad(self, novedad):
        configuracion = GenConfiguracion.objects.filter(pk=1).values('hum_factor', 'hum_salario_minimo', 'hum_auxilio_transporte')[0]
        contrato = novedad.contrato
        salario = contrato.salario
        diferencia = novedad.fecha_hasta - novedad.fecha_desde
        dias = diferencia.days + 1
        if novedad.novedad_tipo_id == 1:
            base_cotizacion = salario
            if contrato.contrato_tipo_id == 5 or contrato.contrato_tipo_id == 6:
                base_cotizacion = configuracion['hum_salario_minimo']
            if novedad.base_cotizacion_propuesto > 0:
                base_cotizacion = novedad.base_cotizacion_propuesto
            valor_dia = base_cotizacion / 30
            valor_hora = valor_dia / configuracion['hum_factor']
            dias_empresa = 0
            dias_entidad = 0
            if dias > 2:
                dias_empresa = 2
                dias_entidad = dias - 2
            novedad.dias_empresa = dias_empresa
            novedad.dias_entidad = dias_entidad
            porcentaje

        if novedad.novedad_tipo_id == 7:
            pago_dia_disfrute = salario / 30
            pago_disfrute = round(pago_dia_disfrute * novedad.dias_disfrutados_reales)
            pago_dia_dinero = salario / 30
            pago_dinero = round(pago_dia_dinero * novedad.dias_dinero)
            #Esto se hace para pagar en dinero lo proporsional en el periodo en disfrute
            pago_dia_dinero = pago_dinero / novedad.dias_disfrutados_reales
            novedad.pago_dia_disfrute = pago_dia_disfrute
            novedad.pago_disfrute = pago_disfrute
            novedad.pago_dia_dinero = pago_dia_dinero
            novedad.pago_dinero = pago_dinero
            novedad.total = pago_disfrute + pago_dinero
        novedad.dias = dias
        novedad.save()

    def perform_create(self, serializer):
        novedad = serializer.save()
        self.liquidar_novedad(novedad)

    def perform_update(self, serializer):
        novedad = serializer.save()
        self.liquidar_novedad(novedad)       

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