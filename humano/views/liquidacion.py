from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from humano.models.liquidacion import HumLiquidacion
from humano.models.concepto import HumConcepto
from general.models.documento_tipo import GenDocumentoTipo
from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from humano.serializers.liquidacion import HumLiquidacionSerializador, HumLiquidacionListaSerializador, HumLiquidacionDetalleSerializador
from general.serializers.documento import GenDocumentoSerializador
from general.serializers.documento_detalle import GenDocumentoDetalleSerializador
from humano.filters.liquidacion import LiquidacionFilter
from utilidades.excel_exportar import ExcelExportar
from servicios.humano.liquidacion import LiquidacionServicio
from servicios.humano.concepto import ConceptoServicio
from django.db import transaction
from django.http import HttpResponse
from humano.formatos.liquidacion import FormatoLiquidacion

class HumLiquidacionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LiquidacionFilter

    queryset = HumLiquidacion.objects.all()   
    serializadores = {
        'lista': HumLiquidacionListaSerializador,
        'detalle': HumLiquidacionDetalleSerializador,
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
            exporter = ExcelExportar(serializer.data, nombre_hoja="liquidaciones", nombre_archivo="liquidaciones.xlsx")
            return exporter.exportar()
        return super().list(request, *args, **kwargs)    
    
    @action(detail=False, methods=["post"], url_path=r'generar',)
    def generar(self, request):
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                liquidacion = HumLiquidacion.objects.get(pk=id)
                if liquidacion.estado_generado == False and liquidacion.estado_aprobado == False:
                    with transaction.atomic():
                        data = {
                            'liquidacion': id,
                            'documento_tipo': 28,
                            'empresa': 1,
                            'fecha': liquidacion.fecha,
                            'fecha_vence': liquidacion.fecha,
                            'fecha_contable': liquidacion.fecha,
                            'fecha_desde': liquidacion.fecha_desde,
                            'fecha_hasta': liquidacion.fecha_hasta,
                            'contrato': liquidacion.contrato_id,
                            'contacto': liquidacion.contrato.contacto_id,
                            'grupo': liquidacion.contrato.grupo_id,                            
                            'dias': liquidacion.dias                    
                        }
                        documento_serializador = GenDocumentoSerializador(data=data)
                        if documento_serializador.is_valid():
                            documento = documento_serializador.save()
                            data_general = {
                                'devengado': 0,
                                'deduccion': 0,
                                'base_cotizacion': 0,
                                'base_prestacion': 0,
                                'base_prestacion_vacacion': 0,
                                'base_licencia': 0
                            }                              
                            data_general_detalle = {
                                'tipo_registro': 'N',
                                'documento': documento.id,
                                'contacto': liquidacion.contrato.contacto_id,                                    
                            }
                            # Cesantia
                            concepto = HumConcepto.objects.get(pk=35)
                            data = data_general_detalle.copy()
                            data['pago'] = round(liquidacion.cesantia)
                            data['concepto'] = concepto.id                            
                            data = ConceptoServicio.datos_documento_detalle(data_general, data, concepto)
                            documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                            if documento_detalle_serializador.is_valid():
                                documento_detalle_serializador.save()
                            else:
                                return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                            
                            # Interes
                            concepto = HumConcepto.objects.get(pk=37)
                            data = data_general_detalle.copy()
                            data['pago'] = round(liquidacion.interes)
                            data['concepto'] = concepto.id                            
                            data = ConceptoServicio.datos_documento_detalle(data_general, data, concepto)
                            documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                            if documento_detalle_serializador.is_valid():
                                documento_detalle_serializador.save()
                            else:
                                return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                              
                            # Prima
                            concepto = HumConcepto.objects.get(pk=33)
                            data = data_general_detalle.copy()
                            data['pago'] = round(liquidacion.prima)
                            data['concepto'] = concepto.id                            
                            data = ConceptoServicio.datos_documento_detalle(data_general, data, concepto)
                            documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                            if documento_detalle_serializador.is_valid():
                                documento_detalle_serializador.save()
                            else:
                                return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                            
                            # Vacacion 
                            concepto = HumConcepto.objects.get(pk=30)
                            data = data_general_detalle.copy()
                            data['pago'] = round(liquidacion.vacacion)
                            data['concepto'] = concepto.id                            
                            data = ConceptoServicio.datos_documento_detalle(data_general, data, concepto)
                            documento_detalle_serializador = GenDocumentoDetalleSerializador(data=data)
                            if documento_detalle_serializador.is_valid():
                                documento_detalle_serializador.save()
                            else:
                                return Response({'validaciones':documento_detalle_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)

                            documento.base_cotizacion = data_general['base_cotizacion']
                            documento.base_prestacion = data_general['base_prestacion']
                            documento.base_prestacion_vacacion = data_general['base_prestacion_vacacion']
                            documento.devengado = data_general['devengado']
                            documento.deduccion = data_general['deduccion']
                            documento.total = data_general['devengado'] - data_general['deduccion']
                            documento.salario = liquidacion.salario
                            documento.save()
                            liquidacion.estado_generado = True  
                            liquidacion.save()
                            return Response({'mensaje': 'Liquidación generada'}, status=status.HTTP_200_OK)                            
                        else:
                            return Response({'validaciones':documento_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                                   
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
                    with transaction.atomic():
                        documentos = GenDocumento.objects.filter(liquidacion_id=id)
                        for documento in documentos:
                            documento_detalles = GenDocumentoDetalle.objects.filter(documento_id=documento.id)
                            documento_detalles.delete()
                        documentos.delete()                                           
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
                    with transaction.atomic():
                        documento_tipo = GenDocumentoTipo.objects.get(pk=28)
                        documentos = GenDocumento.objects.filter(liquidacion_id=id)
                        for documento in documentos:
                            if documento.numero == None or documento.numero == 0:
                                documento.numero = documento_tipo.consecutivo
                                documento_tipo.consecutivo += 1
                            documento.estado_aprobado = True
                            documento.pendiente = documento.total 
                            documento.save()                              
                        documento_tipo.save()                      
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
                with transaction.atomic():
                    documentos = GenDocumento.objects.filter(liquidacion=id)
                    for documento in documentos:
                        if documento.afectado > 0:
                            return Response({'mensaje':f'El documento {documento.id} ya tiene un egreso, no se puede desaprobar la programacion', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 
                        if documento.estado_contabilizado:
                            return Response({'mensaje':f'El documento {documento.id} ya esta contabilizado, no se puede desaprobar la programacion', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                 
                        documento.estado_aprobado = False
                        documento.pendiente = documento.total 
                        documento.save()                                           
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
                LiquidacionServicio.liquidar(liquidacion)                                                                                                                                                
                return Response({'mensaje': 'Liquidacion reliquidada'}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':'La liquidacion ya esta aprobada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
        
    @action(detail=False, methods=["post"], url_path=r'imprimir',)
    def imprimir(self, request):
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                pdf = None
                formato = FormatoLiquidacion()
                pdf = formato.generar_pdf(id)   
                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                    response['Content-Disposition'] = f"attachment; filename=Liquidación_{id}.pdf"
                    return response
            except HumLiquidacion.DoesNotExist:
                return Response({'mensaje':'La liquidación no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)     