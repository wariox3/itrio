from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from humano.models.liquidacion import HumLiquidacion
from general.models.documento import GenDocumento
from humano.serializers.liquidacion import HumLiquidacionSerializador, HumLiquidacionListaSerializador
from humano.filters.liquidacion import LiquidacionFilter

class HumLiquidacionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LiquidacionFilter

    queryset = HumLiquidacion.objects.all()   
    serializadores = {
        'lista': HumLiquidacionListaSerializador,
    }

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return HumLiquidacionSerializador
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
            exporter = ExportarExcel(serializer.data, sheet_name="liquidaciones", filename="liquidaciones.xlsx")
            return exporter.export()
        return super().list(request, *args, **kwargs)    
    
    @action(detail=False, methods=["post"], url_path=r'generar',)
    def generar(self, request):
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                liquidacion = HumLiquidacion.objects.get(pk=id)
                if liquidacion.estado_generado == False and liquidacion.estado_aprobado == False:
                    liquidacion.estado_generado = True  
                    liquidacion.save()
                    return Response({'mensaje': 'Liquidación generada'}, status=status.HTTP_200_OK)

                else:
                    return Response({'mensaje':'La liquidación ya esta generada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)   
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumLiquidacion.DoesNotExist:
            return Response({'mensaje':'La liquidación no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)             

    @action(detail=False, methods=["post"], url_path=r'desgenerar',)
    def desgenerar(self, request):
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                liquidacion = HumLiquidacion.objects.get(pk=id)
                if liquidacion.estado_aprobado == False and liquidacion.estado_generado == True:
                    liquidacion.estado_generado = False  
                    liquidacion.save()
                    return Response({'mensaje': 'Liquidación desgenerada'}, status=status.HTTP_200_OK)

                else:
                    return Response({'mensaje':'La liquidación ya esta aprobada o no esta generada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)   
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumLiquidacion.DoesNotExist:
            return Response({'mensaje':'La liquidación no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)     
        
    @action(detail=False, methods=["post"], url_path=r'aprobar',)
    def aprobar(self, request):
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                liquidacion = HumLiquidacion.objects.get(pk=id)
                if liquidacion.estado_generado == True and liquidacion.estado_aprobado == False:
                    liquidacion.estado_aprobado = True  
                    liquidacion.save()
                    return Response({'mensaje': 'Liquidación aprobada'}, status=status.HTTP_200_OK)

                else:
                    return Response({'mensaje':'La liquidación ya esta generada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)   
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except HumLiquidacion.DoesNotExist:
            return Response({'mensaje':'La liquidación no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)   

    @action(detail=False, methods=["post"], url_path=r'desaprobar',)
    def desaprobar(self, request):                     
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                liquidacion = HumLiquidacion.objects.get(pk=id)
            except HumLiquidacion.DoesNotExist:
                return Response({'mensaje':'La liquidacion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 
            if liquidacion.estado_aprobado == True:                                                                                                                
                '''documentos = GenDocumento.objects.filter(programacion_detalle__programacion_id=id)
                #Validar
                for documento in documentos:
                    if documento.afectado > 0:
                        return Response({'mensaje':f'El documento {documento.id} ya tiene un egreso, no se puede desaprobar la programacion', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 
                    if documento.estado_contabilizado:
                        return Response({'mensaje':f'El documento {documento.id} ya esta contabilizado, no se puede desaprobar la programacion', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 
                for documento in documentos:
                    documento.estado_aprobado = False
                    documento.pendiente = documento.total 
                    documento.save()                        

                    # Desafectar creditos
                    documentos_detalles = GenDocumentoDetalle.objects.filter(documento_id=documento.id)
                    for documento_detalle in documentos_detalles:
                        if documento_detalle.credito:
                            credito = documento_detalle.credito
                            credito.abono -= documento_detalle.pago
                            credito.saldo += documento_detalle.pago
                            credito.cuota_actual -= 1
                            credito.save()

                    # Desafectar contratos
                    contrato = documento.contrato
                    if programacion.pago_tipo_id == 1:
                        contrato.fecha_ultimo_pago = programacion.fecha_desde
                    if programacion.pago_tipo_id == 2:
                        contrato.fecha_ultimo_pago_prima = programacion.fecha_desde
                    if programacion.pago_tipo_id == 3:
                        contrato.fecha_ultimo_pago_cesantia = programacion.fecha_desde
                    contrato.save()  '''                      
                liquidacion.estado_aprobado = False
                liquidacion.save()
                return Response({'mensaje': 'Liquidacion desaprobada'}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':'La liquidacion no esta aprobada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], url_path=r'reliquidar',)
    def reliquidar_action(self, request):                     
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                liquidacion = HumLiquidacion.objects.get(pk=id)
            except HumLiquidacion.DoesNotExist:
                return Response({'mensaje':'La liquidacion no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 
            if liquidacion.estado_aprobado == False:                                                                                                                                                     
                return Response({'mensaje': 'Liquidacion reliquidada'}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':'La liquidacion ya esta aprobada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)        
          