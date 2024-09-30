from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from general.models.documento_impuesto import GenDocumentoImpuesto
from general.models.documento_tipo import GenDocumentoTipo
from general.models.documento_pago import GenDocumentoPago
from general.models.empresa import GenEmpresa
from general.models.contacto import GenContacto
from general.models.configuracion import GenConfiguracion
from humano.models.contrato import HumContrato
from contabilidad.models.cuenta import ConCuenta
from general.serializers.documento import GenDocumentoSerializador, GenDocumentoExcelSerializador, GenDocumentoRetrieveSerializador, GenDocumentoInformeSerializador, GenDocumentoAdicionarSerializador
from general.serializers.documento_detalle import GenDocumentoDetalleSerializador
from general.serializers.documento_impuesto import GenDocumentoImpuestoSerializador
from general.serializers.documento import GenDocumentoReferenciaSerializador
from general.serializers.documento_pago import GenDocumentoPagoSerializador
from general.formatos.factura import FormatoFactura
from general.formatos.cuenta_cobro import FormatoCuentaCobro
from general.formatos.nomina import FormatoNomina
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum, F, Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from utilidades.wolframio import Wolframio
from utilidades.zinc import Zinc
from utilidades.excel import WorkbookEstilos
from decimal import Decimal
from openpyxl import Workbook
from datetime import datetime, timedelta, date
from io import BytesIO
import base64
import openpyxl
import calendar

def transformar_decimal(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = transformar_decimal(value)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            obj[index] = transformar_decimal(value)
    elif isinstance(obj, Decimal):
        return str(obj)
    return obj

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = GenDocumento.objects.all()
    serializer_class = GenDocumentoSerializador
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        raw = request.data
        documentoSerializador = GenDocumentoSerializador(data=raw)
        if documentoSerializador.is_valid():            
            documento_tipo = documentoSerializador.validated_data['documento_tipo']
            documentoSerializador.validated_data['fecha_contable'] = documentoSerializador.validated_data['fecha']
            resolucion = documento_tipo.resolucion        
            documento = documentoSerializador.save(resolucion=resolucion)                        
            documentoRespuesta = documentoSerializador.data 
            detalles = raw.get('detalles')
            pagos = raw.get('pagos')
            if detalles is not None:
                for detalle in detalles:                
                    detalle['documento'] = documento.id
                    detalleSerializador = GenDocumentoDetalleSerializador(data=detalle)
                    if detalleSerializador.is_valid():
                        documentoDetalle = detalleSerializador.save() 
                        impuestos = detalle.get('impuestos')
                        if impuestos is not None:
                            for impuesto in impuestos:
                                datosDocumentoImpuesto = {
                                    "documento_detalle":documentoDetalle.id, 
                                    "impuesto":impuesto['impuesto'],
                                    "base":impuesto['base'],
                                    "porcentaje":impuesto['porcentaje'],
                                    "total":impuesto['total'],
                                    "total_operado":impuesto['total_operado'],
                                    "porcentaje_base":impuesto['porcentaje_base']
                                }
                                documentoImpuestoSerializador = GenDocumentoImpuestoSerializador(data=datosDocumentoImpuesto)
                                if documentoImpuestoSerializador.is_valid():
                                    documentoImpuestoSerializador.save()
                                else:
                                    return Response({'mensaje':'Errores de validacion detalle impuesto', 'codigo':14, 'validaciones': documentoImpuestoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                                
                    else:
                        return Response({'mensaje':'Errores de validacion detalle', 'codigo':14, 'validaciones': detalleSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)            
                documentoDetalles = GenDocumentoDetalle.objects.filter(documento=documento.id)
                documentoDetallesSerializador = GenDocumentoDetalleSerializador(documentoDetalles, many=True)
                detalles = documentoDetallesSerializador.data
                for detalle in detalles:
                    documentoImpuestos = GenDocumentoImpuesto.objects.filter(documento_detalle=detalle['id'])
                    documentoImpuestosSerializador = GenDocumentoImpuestoSerializador(documentoImpuestos, many=True)
                    detalle['impuestos'] = documentoImpuestosSerializador.data
                documentoRespuesta['detalles'] = detalles   
            if pagos is not None:
                for pago in pagos:                
                    pago['documento'] = documento.id
                    pagoSerializador = GenDocumentoPagoSerializador(data=pago)
                    if pagoSerializador.is_valid():
                        documentoPago = pagoSerializador.save() 
                    else:
                        return Response({'mensaje':'Errores de validacion pago', 'codigo':14, 'validaciones': pagoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)            
                documentoRespuesta['pagos'] = pagos                                         
            return Response({'documento': documentoRespuesta}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': documentoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        queryset = GenDocumento.objects.all()
        documento = get_object_or_404(queryset, pk=pk)
        documentoSerializador = GenDocumentoRetrieveSerializador(documento)
        documentoDetalles = GenDocumentoDetalle.objects.filter(documento=pk)
        documentoDetallesSerializador = GenDocumentoDetalleSerializador(documentoDetalles, many=True)
        detalles = documentoDetallesSerializador.data
        for detalle in detalles:
            documentoImpuestos = GenDocumentoImpuesto.objects.filter(documento_detalle=detalle['id'])
            documentoImpuestosSerializador = GenDocumentoImpuestoSerializador(documentoImpuestos, many=True)
            detalle['impuestos'] = documentoImpuestosSerializador.data
        documentoRespuesta = documentoSerializador.data
        documentoRespuesta['detalles'] = detalles
        
        documentoPagos = GenDocumentoPago.objects.filter(documento=pk)
        documentoPagosSerializador = GenDocumentoPagoSerializador(documentoPagos, many=True)
        pagos = documentoPagosSerializador.data
        documentoRespuesta['pagos'] = pagos        
        
        return Response({'documento':documentoRespuesta}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        raw = request.data
        try:
            documento = GenDocumento.objects.get(pk=pk)        
            if documento.estado_aprobado == False:
                documentoSerializador = GenDocumentoSerializador(documento, data=raw, partial=True)
                if documentoSerializador.is_valid():
                    documentoSerializador.save()
                    detalles = raw.get('detalles')
                    if detalles is not None:
                        for detalle in detalles:                
                            if detalle.get('id'):
                                documentoDetalle = GenDocumentoDetalle.objects.get(pk=detalle['id'])
                                detalleSerializador = GenDocumentoDetalleSerializador(documentoDetalle, data=detalle, partial=True)    
                            else:
                                detalle['documento'] = documento.id
                                detalleSerializador = GenDocumentoDetalleSerializador(data=detalle)
                            if detalleSerializador.is_valid():
                                documentoDetalle = detalleSerializador.save() 
                                impuestos = detalle.get('impuestos')
                                if impuestos is not None:
                                    for impuesto in impuestos:
                                        if impuesto.get('id'):
                                            documentoImpuesto = GenDocumentoImpuesto.objects.get(pk=impuesto['id'])
                                            documentoImpuestoSerializador = GenDocumentoImpuestoSerializador(documentoImpuesto, data=impuesto, partial=True)    
                                        else:        
                                            impuesto['documento_detalle'] = documentoDetalle.id                                     
                                            documentoImpuestoSerializador = GenDocumentoImpuestoSerializador(data=impuesto)                            
                                        if documentoImpuestoSerializador.is_valid():
                                            documentoImpuestoSerializador.save()
                                        else:
                                            return Response({'mensaje':'Errores de validacion detalle impuesto', 'codigo':14, 'validaciones': documentoImpuestoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                                                        
                                impuestosEliminados = detalle.get('impuestos_eliminados')
                                if impuestosEliminados is not None:
                                    for documentoImpuesto in impuestosEliminados:                                
                                        documentoImpuesto = GenDocumentoImpuesto.objects.get(pk=documentoImpuesto)
                                        documentoImpuesto.delete()                         
                            else:
                                return Response({'mensaje':'Errores de validacion detalle', 'codigo':14, 'validaciones': detalleSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)            
                    detallesEliminados = raw.get('detalles_eliminados')
                    if detallesEliminados is not None:
                        for detalle in detallesEliminados:                                
                            documentoDetalle = GenDocumentoDetalle.objects.get(pk=detalle)
                            documentoDetalle.delete()
                    documentoDetalles = GenDocumentoDetalle.objects.filter(documento=pk)
                    documentoDetallesSerializador = GenDocumentoDetalleSerializador(documentoDetalles, many=True)
                    detalles = documentoDetallesSerializador.data
                    for detalle in detalles:
                        documentoImpuestos = GenDocumentoImpuesto.objects.filter(documento_detalle=detalle['id'])
                        documentoImpuestosSerializador = GenDocumentoImpuestoSerializador(documentoImpuestos, many=True)
                        detalle['impuestos'] = documentoImpuestosSerializador.data
                    documentoRespuesta = documentoSerializador.data
                    documentoRespuesta['detalles'] = detalles

                    pagos = raw.get('pagos')
                    if pagos is not None:
                        for pago in pagos:                
                            if pago.get('id'):
                                documentoPago = GenDocumentoPago.objects.get(pk=pago['id'])
                                documentoPagoSerializador = GenDocumentoPagoSerializador(documentoPago, data=pago, partial=True)    
                            else:
                                pago['documento'] = documento.id
                                documentoPagoSerializador = GenDocumentoPagoSerializador(data=pago)

                            if documentoPagoSerializador.is_valid():
                                documentoPago = documentoPagoSerializador.save()                         
                            else:
                                return Response({'mensaje':'Errores de validacion pago', 'codigo':14, 'validaciones': documentoPagoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)            
                    pagosEliminados = raw.get('pagos_eliminados')
                    if pagosEliminados is not None:
                        for pago in pagosEliminados:                                
                            documentoPago = GenDocumentoPago.objects.get(pk=pago)
                            documentoPago.delete()
                    documentoPagos = GenDocumentoPago.objects.filter(documento=pk)
                    documentoPagosSerializador = GenDocumentoPagoSerializador(documentoPagos, many=True)
                    pagos = documentoPagosSerializador.data
                    documentoRespuesta['pagos'] = pagos   
                    return Response({'documento': documentoRespuesta}, status=status.HTTP_200_OK)                    
                return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': documentoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje':'Los documentos aprobados no se pueden modificar', 'codigo':14}, status=status.HTTP_400_BAD_REQUEST)
        except GenDocumento.DoesNotExist:
            return Response({'mensaje': 'El documento no existe', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):        
        instance = self.get_object()
        if instance.estado_aprobado:
                return Response({'mensaje': 'No se puede eliminar un documento aprobado.'}, status=status.HTTP_400_BAD_REQUEST)
        if instance.documento_tipo_id == 15:
            nominas = GenDocumento.objects.filter(documento_referencia_id=instance.id)
            nominas.update(documento_referencia_id=None)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"], url_path=r'eliminar',)
    def eliminar(self, request):
        try:
            raw = request.data
            documentos = raw.get('documentos')
            if documentos:  
                for documento in documentos:
                    documentoEliminar = GenDocumento.objects.get(pk=documento)  
                    if documentoEliminar:
                        if documentoEliminar.estado_aprobado == False:
                            if not documentoEliminar.detalles.exists():
                                if not documentoEliminar.documentos_detalles_documento_afectado_rel.exists():
                                    documentoEliminar.delete()   
                                else:
                                    return Response({'mensaje':'El documento con id ' + str(documentoEliminar.id) + ' esta afectado con algunos detalles', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                                                                        
                            else:                            
                                return Response({'mensaje':'El documento con id ' + str(documentoEliminar.id) + ' no se puede eliminar por que tiene detalles', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                                    
                        else:
                            return Response({'mensaje':'El documento con id ' + str(documentoEliminar.id) + ' no se puede eliminar por que se encuentra aprobado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'mensaje':'Registros eliminados'}, status=status.HTTP_200_OK)
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except GenDocumento.DoesNotExist:
            return Response({'mensaje':'El documento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'aprobar',)
    def aprobar(self, request):        
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                documento = GenDocumento.objects.get(pk=id)
                consecutivo = 0
                documentoTipo = GenDocumentoTipo.objects.get(id=documento.documento_tipo_id)
                if documento.numero is None:
                    consecutivo = documentoTipo.consecutivo
                else: 
                    consecutivo = documento.numero
                respuesta = self.validacion_aprobar(id, consecutivo)
                if respuesta['error'] == False:                         
                    if documento.numero is None:
                        documento.numero = documentoTipo.consecutivo
                        documentoTipo.consecutivo += 1
                        documentoTipo.save()                
                    documento.estado_aprobado = True
                    if documento.documento_tipo.documento_clase_id in (100,101,102,300,301,302,303):
                        documento.pendiente = documento.total - documento.afectado    
                    if documento.documento_tipo.documento_clase_id == 200:
                        documento_detalles = GenDocumentoDetalle.objects.filter(documento_id=id).exclude(documento_afectado_id__isnull=True)
                        for documento_detalle in documento_detalles:
                            documento_afectado = documento_detalle.documento_afectado                        
                            documento_afectado.afectado += documento_detalle.pago
                            documento_afectado.pendiente = documento_afectado.total - documento_afectado.afectado
                            documento_afectado.save(update_fields=['afectado', 'pendiente'])
                    documento.save()
                    return Response({'estado_aprobado': True}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':respuesta['mensaje'], 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
            except GenDocumento.DoesNotExist:
                return Response({'mensaje':'El documento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'anular',)
    def anular(self, request):
        try:
            raw = request.data
            id = raw.get('id')
            if id:
                documento = GenDocumento.objects.get(pk=id)                
                respuesta = self.validacion_anular(id)
                if respuesta['error'] == False:    
                    documento_detalles = GenDocumentoDetalle.objects.filter(documento_id=id)                                          
                    for documento_detalle in documento_detalles:                                               
                        documento_detalle.cantidad = 0
                        documento_detalle.precio = 0
                        documento_detalle.porcentaje_descuento = 0
                        documento_detalle.descuento = 0
                        documento_detalle.subtotal = 0
                        documento_detalle.impuesto = 0
                        documento_detalle.base_impuesto = 0
                        documento_detalle.total = 0
                        documento_detalle.total_bruto = 0
                        documento_detalle.save(update_fields=['cantidad', 'precio', 'porcentaje_descuento', 'descuento', 'subtotal', 'impuesto', 'base_impuesto', 'total', 'total_bruto'])
                        documento_impuestos = GenDocumentoImpuesto.objects.filter(documento_detalle_id=documento_detalle.id)
                        for documento_impuesto in documento_impuestos:
                            documento_impuesto.base = 0
                            documento_impuesto.total = 0 
                            documento_impuesto.save(update_fields=['base','total'])
                    documento.estado_anulado = True  
                    documento.subtotal = 0
                    documento.total = 0
                    documento.total_bruto = 0
                    documento.base_impuesto = 0
                    documento.descuento = 0
                    documento.impuesto = 0
                    documento.pendiente = 0
                    documento.save(update_fields=['estado_anulado', 'subtotal', 'total', 'total_bruto', 'pendiente', 'base_impuesto', 'descuento', 'impuesto'])
                    return Response({'estado_anulado': True}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':respuesta['mensaje'], 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except GenDocumento.DoesNotExist:
            return Response({'mensaje':'El documento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
   
    @action(detail=False, methods=["post"], url_path=r'imprimir',)
    def imprimir(self, request):
        raw = request.data
        id = raw.get('documento_id')
        if id:
            try:
                pdf = None
                documento = GenDocumento.objects.get(pk=id)
                if documento.documento_tipo_id in (1,2,3):
                    documento_consulta = self.consulta_imprimir(id)
                    configuracion = GenConfiguracion.objects.select_related('formato_factura').filter(empresa_id=1).values().first()
                    if configuracion['formato_factura'] == 'F':
                        formato = FormatoFactura()
                        pdf = formato.generar_pdf(documento_consulta, configuracion)  
                        numero_documento = documento_consulta.get('numero')
                        tipo_documento = documento_consulta.get('documento_tipo__documento_clase_id')
                        nombres_archivo = {
                            100: f"Factura_{numero_documento}.pdf" if numero_documento else "Factura.pdf",
                            101: f"NotaCredito{numero_documento}.pdf" if numero_documento else "NotaCredito.pdf",
                            102: f"NotaDebito{numero_documento}.pdf" if numero_documento else "NotaDebito.pdf"
                        }
                        nombre_archivo = nombres_archivo.get(tipo_documento)            
                    else:     
                        formato = FormatoCuentaCobro()
                        pdf = formato.generar_pdf(documento_consulta, configuracion)
                        numero_documento = documento_consulta.get('numero')
                        tipo_documento = documento_consulta.get('documento_tipo__documento_clase_id')
                        nombres_archivo = {
                            100: f"CuentaCobro{numero_documento}.pdf" if numero_documento else "CuentaCobro.pdf",
                            101: f"NotaCredito{numero_documento}.pdf" if numero_documento else "NotaCredito.pdf",
                            102: f"NotaDebito{numero_documento}.pdf" if numero_documento else "NotaDebito.pdf"
                        }
                        nombre_archivo = nombres_archivo.get(tipo_documento)
                
                if documento.documento_tipo_id == 14:
                    formato = FormatoNomina()
                    pdf = formato.generar_pdf(documento)              
                    nombre_archivo = f"nomina_{documento.numero}.pdf" if documento.numero else "nomina.pdf"       

                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
                    return response
                else:
                    return Response({'mensaje':'El documento no tiene un formato', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
            except GenDocumento.DoesNotExist:
                return Response({'mensaje':'El documento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)            
    
    @action(detail=False, methods=["post"], url_path=r'emitir',)
    def emitir(self, request):
        try:
            raw = request.data
            id = raw.get('documento_id')
            if id:
                documento = GenDocumento.objects.get(pk=id)
                if documento.estado_aprobado == True:
                    empresa = GenEmpresa.objects.get(pk=1)
                    if empresa.rededoc_id:
                        if documento.estado_electronico_enviado == False: 
                            if documento.numero: 
                                if documento.documento_tipo_id in [1,2,3,11,12]:
                                    if documento.resolucion: 
                                        #Las facturas y documento soporte toman prefijo de la resolucion
                                        prefijo = documento.resolucion.prefijo
                                        documento_referencia_id = None
                                        forma_pago = 2
                                        if documento.plazo_pago_id == 1:
                                            forma_pago = 1                                            
                                        if documento.documento_tipo.documento_clase_id == 101:
                                            prefijo = "NC"
                                        if documento.documento_tipo.documento_clase_id == 102:
                                            prefijo = "ND" 
                                        if documento.documento_tipo.documento_clase_id == 304:
                                            prefijo = "DSAJ"
                                        datos_factura = {
                                            "cuentaId": empresa.rededoc_id,
                                            "documentoClaseId" : documento.documento_tipo_id,
                                            "documentoClienteId": documento.id,
                                            "documento" : {
                                                "ambiente" : 1,
                                                "prefijo" : prefijo,
                                                "numero" : documento.numero,
                                                "fecha" : str(documento.fecha),
                                                "hora" : str("12:00:00-05:00"),
                                                "fecha_vence" : str(documento.fecha_vence),
                                                "tipo_operacion" : str(10),
                                                "moneda" : "COP",
                                                "orden_compra": documento.orden_compra,
                                                "resolucion" : str(documento.resolucion.numero),
                                                "forma_pago" : forma_pago,
                                                "cantidad_detalles" :1,
                                                "subtotal" : str(documento.subtotal),
                                                "subtotal_mas_impuestos" : str(documento.subtotal + documento.impuesto),
                                                "base" : str(documento.base_impuesto),
                                                "total_impuestos" : str(documento.impuesto),
                                                "total_descuentos" : str(documento.descuento),
                                                "total_cargos" : str(0),
                                                "total_anticipos" : str(0),
                                                "total_documento" : str(documento.total),
                                                "total_iva" : str(0),
                                                "total_consumo" : str(0),
                                                "total_ica" : str(0),
                                                "documento_referencia": documento_referencia_id,
                                                "adquiriente" : {
                                                    "identificacion" : documento.contacto.identificacion.codigo,
                                                    "numero_identificacion" : documento.contacto.numero_identificacion,
                                                    "digito_verificacion" : documento.contacto.digito_verificacion,
                                                    "razon_social" : documento.contacto.nombre_corto,
                                                    "pais" : "CO",
                                                    "ciudad" : documento.contacto.ciudad.nombre,
                                                    "departamento" : documento.contacto.ciudad.estado.nombre,
                                                    "direccion" : documento.contacto.direccion,
                                                    "obligaciones" : "0-99",
                                                    "nombres" : documento.contacto.nombre1,
                                                    "apellidos" : documento.contacto.apellido1,
                                                    "correo" : documento.contacto.correo,
                                                    "telefono" : documento.contacto.telefono,
                                                    "tipo_organizacion_juridica" : documento.contacto.tipo_persona.id,
                                                    "regimen_tributario" : documento.contacto.regimen.codigo_interface,
                                                    "codigo_postal" : documento.contacto.ciudad.codigo_postal,
                                                    "responsable" : 1,
                                                    "nacional" : 1
                                                },
                                            }
                                        }
                                        arr_medio_pago = []

                                        arr_medio_pago.append({
                                            "medio_pago": 31,
                                            "descripcion": "",
                                        })

                                        datos_factura['documento']['medios_pago'] = arr_medio_pago

                                        arr_item = []
                                        cantidad_items = 0
                                        impuestos_agrupados = {}
                                        documentoDetalles = GenDocumentoDetalle.objects.filter(documento=id)
                                        for documentoDetalle in documentoDetalles:
                                            arr_impuestos = []
                                            documentoImpuestoDetalles = GenDocumentoImpuesto.objects.filter(documento_detalle=documentoDetalle.id)
                                            for documentoImpuestoDetalle in documentoImpuestoDetalles:
                                                impuesto_id = documentoImpuestoDetalle.impuesto_id
                                                total = documentoImpuestoDetalle.total
                                                arr_impuestos.append({
                                                    "tipo_impuesto" : documentoImpuestoDetalle.impuesto_id,
                                                    "total" : str(documentoImpuestoDetalle.total),
                                                    "porcentual" : str(documentoImpuestoDetalle.porcentaje)
                                                })

                                                if impuesto_id in impuestos_agrupados:
                                                    impuestos_agrupados[impuesto_id] += total
                                                else:
                                                    impuestos_agrupados[impuesto_id] = total

                                            cantidad_items += 1
                                            arr_item.append({
                                                "consecutivo": cantidad_items,
                                                "codigo": documentoDetalle.item.codigo,
                                                "descripcion" : documentoDetalle.item.nombre,
                                                "marca" : "",
                                                "modelo" : "",
                                                "observacion" : "",
                                                "cantidad" : str(documentoDetalle.cantidad),
                                                "cantidad_empque": str(documentoDetalle.cantidad),
                                                "obserquio" : str(0),
                                                "precio_unitario" : str(documentoDetalle.precio),
                                                "precio_referencia" : str(documentoDetalle.precio),
                                                "valor" : str(documentoDetalle.precio),
                                                "total_descuentos" : str(documentoDetalle.descuento),
                                                "total_cargos" : str(0),
                                                "total_impuestos" : str(documentoDetalle.impuesto),
                                                "base" : str(documentoDetalle.base_impuesto),
                                                "subtotal" : str(documentoDetalle.subtotal),
                                                "impuestos" : arr_impuestos
                                            })
                                        datos_factura['documento']['cantidad_detalles'] = cantidad_items
                                        arr_impuestos = []
                                        for impuesto_id, total in impuestos_agrupados.items():
                                            arr_impuestos.append({
                                                "tipo_impuesto": impuesto_id,
                                                "total": str(total),
                                                "porcentual" : str(19.00)
                                            })
                                        
                                        datos_factura['documento']['detalles'] = arr_item
                                        datos_factura['doc_cantidad_item'] = cantidad_items
                                        datos_factura['documento']['impuestos'] = arr_impuestos
                                        wolframio = Wolframio()
                                        respuesta = wolframio.emitir(datos_factura)
                                        if respuesta['error'] == False: 
                                            documento.estado_electronico_enviado = True
                                            documento.electronico_id = respuesta['id']
                                            documento.save()                                        
                                        else:
                                            return Response({'mensaje': respuesta['mensaje'], 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)
                                    else:
                                        return Response({'mensaje': 'La factura no cuenta con una resolución asociada', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
                                if documento.documento_tipo_id in [15]:                                
                                    prefijo = "NE"                                
                                    datos = {
                                        "cuentaId": empresa.rededoc_id,
                                        "documentoClaseId" : documento.documento_tipo_id,
                                        "documentoClienteId": documento.id,
                                        "documento" : {
                                            "ambiente" : 1,
                                            "prefijo" : prefijo,
                                            "numero" : documento.numero,
                                            "fecha" : str(documento.fecha),
                                            "hora" : str("12:00:00-05:00"),
                                            "devengado":str(documento.devengado),
                                            "deduccion":str(documento.deduccion),
                                            "total_documento" : str(documento.total),                                                                                                                                                                                                    
                                            "fecha_desde":str(documento.fecha),
                                            "fecha_hasta":str(documento.fecha_hasta),                                                                                                                    
                                            "empleado" : {
                                                "codigo": documento.contacto_id,
                                                "identificacion" : documento.contacto.identificacion.codigo,
                                                "numero_identificacion" : documento.contacto.numero_identificacion,
                                                "digito_verificacion" : documento.contacto.digito_verificacion,
                                                "razon_social" : documento.contacto.nombre_corto,
                                                "pais" : "CO",
                                                "ciudad" : documento.contacto.ciudad.nombre,
                                                "ciudad_codigo_postal" : documento.contacto.ciudad.codigo_postal,
                                                "departamento" : documento.contacto.ciudad.estado.codigo,
                                                "direccion" : documento.contacto.direccion,                                                
                                                "nombre1" : documento.contacto.nombre1,
                                                "nombre2" : documento.contacto.nombre2,
                                                "apellido1" : documento.contacto.apellido1,
                                                "apellido2" : documento.contacto.apellido2,
                                                "correo" : documento.contacto.correo,
                                                "telefono" : documento.contacto.telefono,
                                                "tipo_organizacion_juridica" : documento.contacto.tipo_persona.id,
                                                "regimen_tributario" : documento.contacto.regimen.codigo_interface,                                                
                                                "cuenta":documento.contacto.numero_cuenta,
                                                "banco":documento.contacto.banco.nombre, 
                                                "responsable" : 1,
                                                "nacional" : 1
                                            },
                                            "contrato" : {
                                                "fecha_desde":str(documento.contrato.fecha_desde),
                                                "salario":str(documento.salario),
                                                "salario_intergral":documento.contrato.salario_integral,
                                                "tipo_cotizante":documento.contrato.tipo_cotizante.codigo,
                                                "subtipo_cotizante":documento.contrato.subtipo_cotizante.codigo,
                                                "contrato_tipo":documento.contrato.contrato_tipo_id,                                            
                                                "ciudad_labora" : documento.contrato.ciudad_labora.nombre,
                                                "ciudad_labora_codigo_postal" : documento.contrato.ciudad_labora.codigo_postal,
                                                "estado_labora_codigo_postal":documento.contrato.ciudad_labora.estado.codigo,
                                            },
                                        }
                                    }           
                                    
                                    detalle = {
                                        'valido': True,
                                        'Devengados': {
                                            'Basico': {
                                                'DiasTrabajados': 0,
                                                'SueldoTrabajado': 0
                                            },
                                            "Transporte": {
                                                "AuxilioTransporte": 0,
                                                "ViaticoManuAlojS": 0,
                                                "ViaticoManuAlojNS": 0
                                            },
                                            "OtrosConceptos": [],
                                            "Bonificaciones": [],
                                            "Auxilios": [],
                                            "HorasExtras": {
                                                "HED": [],
                                                "HEN": [],
                                                "HRN": [],
                                                "HEDDF": [],
                                                "HRDDF": [],
                                                "HENDF": [],
                                                "HRNDF": [],
                                            },
                                            "Compensaciones": [],
                                            "HuelgasLegales": [],
                                            "BonoEPCTVs": [],
                                            "Comisiones": [],
                                            "PagosTerceros": [],
                                            "Anticipos": [],
                                            "Vacaciones": {
                                                "VacacionesComunes": [],
                                                "VacacionesCompensadas": []
                                            },
                                            "Primas": {
                                                'Cantidad':0,
                                                'Pago':0,
                                                'PagoNS':0
                                            },
                                            "Cesantias": {
                                                "Pago": 0,
                                                "Porcentaje": 0,
                                                "PagoIntereses": 0
                                            },
                                            "Incapacidades": [],
                                            "Licencias": {
                                                "LicenciaMP": [],
                                                "LicenciaR": [],
                                                "LicenciaNR": [],
                                            },
                                            'Dotacion': 0,
                                            'ApoyoSost': 0,
                                            'Teletrabajo': 0,
                                            'BonifRetiro': 0,
                                            'Indemnizacion': 0,
                                            'Reintegro': 0,
                                        },
                                        'Deducciones': {
                                            "Salud": {
                                                "Porcentaje": 0,
                                                "Deduccion": 0
                                            },
                                            "FondoPension": {
                                                "Porcentaje": 0,
                                                "Deduccion": 0
                                            },
                                            "FondoSP": {
                                                "Porcentaje": 0,
                                                "DeduccionSP": 0,
                                                "PorcentajeSub": 0,
                                                "DeduccionSub": 0
                                            },
                                            "Sindicatos": [],
                                            "Sanciones": [],
                                            "Libranzas": [],
                                            "PagosTerceros": [],
                                            "Anticipos": [],
                                            "OtrasDeducciones": [],
                                            'PensionVoluntaria': 0,
                                            'RetencionFuente': 0,
                                            'AFC': 0,
                                            'Cooperativa': 0,
                                            'EmbargoFiscal': 0,
                                            'PlanComplementarios': 0,
                                            'Educacion': 0,
                                            'Reintegro': 0,
                                            'Deuda': 0,
                                        }
                                    }
                                    datos['documento']['detalle'] = detalle
                                    documento_detalles = GenDocumentoDetalle.objects.filter(
                                        documento__documento_referencia_id=id
                                    ).values(
                                        'id', 'operacion', 'porcentaje', 'dias', 'cantidad', 'pago','concepto_id', 'concepto__nombre', 'concepto__concepto_tipo_id'
                                    )
                                    print(documento_detalles.query)
                                    for documento_detalle in documento_detalles:                                        
                                        fecha = documento.fecha
                                        fecha_desde_extra = fecha.strftime('%Y-%m-%d') + "T11:00:00"
                                        fecha_hasta_extra = fecha.strftime('%Y-%m-%d') + "T12:00:00"                                        
                                        if documento_detalle['operacion'] == 1:
                                            if documento_detalle['concepto__concepto_tipo_id'] == 1:
                                                dias_basico = documento_detalle['dias'] if documento_detalle['dias'] != 0 else 1
                                                detalle['Devengados']['Basico']['DiasTrabajados'] += dias_basico
                                                detalle['Devengados']['Basico']['SueldoTrabajado'] += documento_detalle['pago']                                                

                                            if documento_detalle['concepto__concepto_tipo_id'] == 7:
                                                detalle['Devengados']['Transporte']['AuxilioTransporte'] += documento_detalle['pago']

                                            if documento_detalle['concepto__concepto_tipo_id'] == 3:                                                                                                                                            
                                                detalle['Devengados']['OtrosConceptos'].append({
                                                        'DescripcionConcepto': documento_detalle['concepto__nombre'],
                                                        'ConceptoS': documento_detalle['pago'],
                                                        'ConceptoNS': 0
                                                        })
                                                
                                            if documento_detalle['concepto__concepto_tipo_id'] == 4:                                                                                                                                            
                                                detalle['Devengados']['OtrosConceptos'].append({
                                                        'DescripcionConcepto': documento_detalle['concepto__nombre'],
                                                        'ConceptoS': 0,
                                                        'ConceptoNS': documento_detalle['pago']
                                                        })
                                            
                                            if documento_detalle['concepto__concepto_tipo_id'] == 2:
                                                # No se pueden cambiar los porcentajes
                                                if documento_detalle['concepto_id'] in [5,3]:
                                                    detalle['Devengados']['HorasExtras']['HED'].append({
                                                        "Id":0,
                                                        "HoraInicio":fecha_desde_extra,
                                                        "HoraFin":fecha_hasta_extra,
                                                        "Cantidad":documento_detalle['cantidad'],
                                                        "Porcentaje":25,
                                                        "Pago":documento_detalle['pago']
                                                        })                                                    
                                                if documento_detalle['concepto_id'] in [6,4]:
                                                    detalle['Devengados']['HorasExtras']['HEN'].append({
                                                        "Id":0,
                                                        "HoraInicio":fecha_desde_extra,
                                                        "HoraFin":fecha_hasta_extra,
                                                        "Cantidad":documento_detalle['cantidad'],
                                                        "Porcentaje":75,
                                                        "Pago":documento_detalle['pago']
                                                        }) 
                                                if documento_detalle['concepto_id'] in [9,2]:
                                                    detalle['Devengados']['HorasExtras']['HRN'].append({
                                                        "Id":0,
                                                        "HoraInicio":fecha_desde_extra,
                                                        "HoraFin":fecha_hasta_extra,
                                                        "Cantidad":documento_detalle['cantidad'],
                                                        "Porcentaje":35,
                                                        "Pago":documento_detalle['pago']
                                                        }) 
                                                if documento_detalle['concepto_id'] in [7]:
                                                    detalle['Devengados']['HorasExtras']['HEDDF'].append({
                                                        "Id":0,
                                                        "HoraInicio":fecha_desde_extra,
                                                        "HoraFin":fecha_hasta_extra,
                                                        "Cantidad":documento_detalle['cantidad'],
                                                        "Porcentaje":100,
                                                        "Pago":documento_detalle['pago']
                                                        }) 
                                                if documento_detalle['concepto_id'] in [10]:
                                                    detalle['Devengados']['HorasExtras']['HRDDF'].append({
                                                        "Id":0,
                                                        "HoraInicio":fecha_desde_extra,
                                                        "HoraFin":fecha_hasta_extra,
                                                        "Cantidad":documento_detalle['cantidad'],
                                                        "Porcentaje":75,
                                                        "Pago":documento_detalle['pago']
                                                        }) 
                                                if documento_detalle['concepto_id'] in [8]:
                                                    detalle['Devengados']['HorasExtras']['HENDF'].append({
                                                        "Id":0,
                                                        "HoraInicio":fecha_desde_extra,
                                                        "HoraFin":fecha_hasta_extra,
                                                        "Cantidad":documento_detalle['cantidad'],
                                                        "Porcentaje":150,
                                                        "Pago":documento_detalle['pago']
                                                        }) 
                                                if documento_detalle['concepto_id'] in [11]:
                                                    detalle['Devengados']['HorasExtras']['HRNDF'].append({
                                                        "Id":0,
                                                        "HoraInicio":fecha_desde_extra,
                                                        "HoraFin":fecha_hasta_extra,
                                                        "Cantidad":documento_detalle['cantidad'],
                                                        "Porcentaje":110,
                                                        "Pago":documento_detalle['pago']
                                                        })                                                                                                                                                                                                                                                                                                 

                                            if documento_detalle['concepto__concepto_tipo_id'] == 18:
                                                detalle['Devengados']['Vacaciones']['VacacionesComunes'].append({
                                                        'FechaInicio': None,
                                                        'FechaFin': None,
                                                        'Cantidad': documento_detalle['dias'],
                                                        'Pago': documento_detalle['pago']
                                                        })

                                            if documento_detalle['concepto__concepto_tipo_id'] == 19:
                                                detalle['Devengados']['Vacaciones']['VacacionesCompensadas'].append({
                                                        'Cantidad': 0,
                                                        'Pago': documento_detalle['pago']
                                                })

                                            if documento_detalle['concepto__concepto_tipo_id'] in [20,21]:
                                                detalle['Devengados']['Primas']['PagoNS'] += documento_detalle['pago']

                                            if documento_detalle['concepto__concepto_tipo_id'] in [22,23]:
                                                detalle['Devengados']['Cesantias']['Pago'] += documento_detalle['pago']

                                            if documento_detalle['concepto__concepto_tipo_id'] in [24,25]:
                                                detalle['Devengados']['Cesantias']['PagoIntereses'] += documento_detalle['pago']

                                            if documento_detalle['concepto__concepto_tipo_id'] == 12:
                                                detalle['Devengados']['Incapacidades'].append({
                                                    'FechaInicio': None,
                                                    'FechaFin': None,
                                                    'Cantidad':documento_detalle['dias'],
                                                    'Tipo':1,
                                                    'Pago':documento_detalle['pago']
                                                })
                                            
                                            if documento_detalle['concepto__concepto_tipo_id'] == 13:
                                                detalle['Devengados']['Incapacidades'].append({
                                                    'FechaInicio': None,
                                                    'FechaFin': None,
                                                    'Cantidad':documento_detalle['dias'],
                                                    'Tipo':3,
                                                    'Pago':documento_detalle['pago']
                                                })  

                                            if documento_detalle['concepto__concepto_tipo_id'] == 14:
                                                detalle['Devengados']['Licencias']['LicenciaMP'].append({
                                                    "FechaInicio":None,
                                                    "FechaFin":None,
                                                    "Cantidad":0,
                                                    "Pago":documento_detalle['pago']
                                                })

                                            if documento_detalle['concepto__concepto_tipo_id'] in [15,16]:
                                                detalle['Devengados']['Licencias']['LicenciaR'].append({
                                                    "FechaInicio":None,
                                                    "FechaFin":None,
                                                    "Cantidad":0,
                                                    "Pago":documento_detalle['pago']
                                                })

                                            if documento_detalle['concepto__concepto_tipo_id'] in [17]:
                                                detalle['Devengados']['Licencias']['LicenciaNR'].append({
                                                    "FechaInicio":None,
                                                    "FechaFin":None,
                                                    "Cantidad":0,
                                                    "Pago":documento_detalle['pago']
                                                })                                                
                                                
                                        if documento_detalle['operacion'] == -1:        
                                            if documento_detalle['concepto__concepto_tipo_id'] == 5:
                                                detalle['Deducciones']['Salud']['Porcentaje'] = documento_detalle['porcentaje']
                                                detalle['Deducciones']['Salud']['Deduccion'] += documento_detalle['pago']

                                            if documento_detalle['concepto__concepto_tipo_id'] == 6:
                                                detalle['Deducciones']['FondoPension']['Porcentaje'] = documento_detalle['porcentaje']
                                                detalle['Deducciones']['FondoPension']['Deduccion'] += documento_detalle['pago']

                                            if documento_detalle['concepto__concepto_tipo_id'] == 8:                                                                                                                                            
                                                detalle['Deducciones']['Deuda'] += documento_detalle['pago']

                                            if documento_detalle['concepto__concepto_tipo_id'] == 9:
                                                detalle['Deducciones']['FondoSP']['Porcentaje'] = documento_detalle['porcentaje']
                                                detalle['Deducciones']['FondoSP']['DeduccionSP'] += documento_detalle['pago']

                                            if documento_detalle['concepto__concepto_tipo_id'] == 10:
                                                detalle['Deducciones']['RetencionFuente'] += documento_detalle['pago']

                                            if documento_detalle['concepto__concepto_tipo_id'] == 11:                                                                                                                                            
                                                detalle['Deducciones']['OtrasDeducciones'].append(documento_detalle['pago'])

                                    datos = transformar_decimal(datos)
                                    '''wolframio = Wolframio()
                                    respuesta = wolframio.emitir(datos)
                                    if respuesta['error'] == False: 
                                        documento.estado_electronico_enviado = True
                                        documento.electronico_id = respuesta['id']
                                        documento.save()                                        
                                    else:
                                        return Response({'mensaje': respuesta['mensaje'], 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)'''
                                return Response({'mensaje': 'Documento emitido correctamente', 'codigo': 15}, status=status.HTTP_200_OK)
                                #return Response(datos, status=status.HTTP_200_OK)
                            else:
                                return Response({'mensaje': 'La factura no cuenta con un número', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'mensaje': "El documento ya fue enviado", 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)                        
                    else:  
                        return Response({'mensaje': 'La empresa no se encuentra activada para emitir documentos electronicos', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje': 'El documento no se puede emitir ya que no está aprobado', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)                
        except GenDocumento.DoesNotExist:
            return Response({'mensaje': 'El documento no existe', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path=r'electronico_respuesta_emitir', permission_classes=[permissions.AllowAny])
    def electronico_respuesta_emitir(self, request):
        raw = request.data
        documento_id = raw.get('documento_id')
        qr = raw.get('qr')
        cue = raw.get('cue')
        fecha_validacion = raw.get('fecha_validacion')
        if documento_id and qr and cue and fecha_validacion:
            try:
                documento = GenDocumento.objects.get(pk=documento_id)
                if documento.estado_electronico_enviado:
                    fecha_validacion_obj = datetime.strptime(fecha_validacion, '%Y-%m-%d %H:%M:%S')
                    documento.qr = qr
                    documento.cue = cue
                    documento.fecha_validacion = fecha_validacion_obj
                    documento.estado_electronico = True
                    documento.save()                
                    self.notificar(documento_id)
                    return Response({'respuesta':True}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'No se puede entregar una respuesta porque el documento no se ha enviado'}, status=status.HTTP_400_BAD_REQUEST)
            except GenDocumento.DoesNotExist:
                return Response({'mensaje': 'El documento no existe', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path=r'notificar')
    def electronico_notificar(self, request):
        raw = request.data
        documento_id = raw.get('documento_id')
        if documento_id:
            respuesta = self.notificar(documento_id)
            if respuesta['error'] == False:
                return Response({'mensaje': 'notificado'}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje': respuesta['mensaje'], 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)      
        else:
            return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)  

    @action(detail=False, methods=["post"], url_path=r'renotificar')
    def electronico_renotificar(self, request):
        raw = request.data
        documento_id = raw.get('documento_id')
        if documento_id:
            try:
                documento = GenDocumento.objects.get(id=documento_id)
                if documento.estado_electronico_notificado == True:                    
                    if documento.electronico_id:
                        wolframio = Wolframio()
                        respuesta = wolframio.renotificar(documento.electronico_id, documento.contacto.correo)
                        if respuesta['error'] == False: 
                            return Response({'mensaje': 'Documento re-notificado con éxito'}, status=status.HTTP_200_OK)           
                        else:
                            return Response({'mensaje': f"{respuesta['mensaje']}", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)                    
                    else:
                        return Response({'mensaje': 'El documento esta marcado como notificado pero no tiene electronico_id', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)    
                else:                      
                    return Response({'mensaje': 'El documento nunca ha sido notificado', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
            except GenDocumento.DoesNotExist:
                return Response({'mensaje': 'El documento no existe', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)     
        else:
            return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=False, methods=["post"], url_path=r'electronico_log')
    def electronico_log(self, request):
        raw = request.data
        documento_id = raw.get('documento_id')
        if documento_id:
            try:
                documento = GenDocumento.objects.get(id=documento_id)
                if documento.estado_electronico_notificado == True:                    
                    if documento.electronico_id:
                        empresa = GenEmpresa.objects.get(pk=1)
                        if empresa.rededoc_id:                       
                            zinc = Zinc()                        
                            respuesta = zinc.log_envio(empresa.rededoc_id, documento.electronico_id)
                            if respuesta['error'] == False: 
                                return Response({'log': respuesta['log']}, status=status.HTTP_200_OK)
                            else:
                                return Response({'mensaje': f"{respuesta['mensaje']}", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)                                                                                                                    
                        else:
                            return Response({'mensaje': 'La empresa no esta activa en facturacion electronica', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'mensaje': 'El documento esta marcado como notificado pero no tiene electronico_id', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)    
                else:                      
                    return Response({'mensaje': 'El documento nunca ha sido notificado', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
            except GenDocumento.DoesNotExist:
                return Response({'mensaje': 'El documento no existe', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)     
        else:
            return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=False, methods=["post"], url_path=r'proceso_corregir_pendiente')
    def proceso_corregir_pendiente(self, request):
        #update gen_documento as d set cobrar = d.total from gen_documento_tipo as dt where d.documento_tipo_id = dt.id and dt.documento_clase_id in (100, 101, 102);
        resultados = GenDocumento.objects.annotate(total_pago=Sum('detalles__pago'))
        for documento in resultados:
            total_pago = documento.total_pago if documento.total_pago is not None else Decimal('0.00')
            documento.afectado = total_pago 
            documento.pendiente = documento.total - documento.afectado           
            documento.save()
            #print(f"Documento: {documento.id}, Total Pago: {documento.total_pago}")
        return Response({'mensaje':'Proceso finalizado con exito'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path=r'resumen-cobrar',)
    def resumen_cobrar(self, request):      
        fecha_actual = timezone.now().date()
        resumen = GenDocumento.objects.filter(
            documento_tipo_id=1, estado_aprobado=True
            ).aggregate(cantidad=Count('id'), saldo_pendiente=Sum('pendiente'))
        resumen_vigente = GenDocumento.objects.filter(
            documento_tipo_id=1, estado_aprobado=True, fecha_vence__gte=fecha_actual
            ).aggregate(cantidad=Count('id'), saldo_pendiente=Sum('pendiente'))
        resumen_vencido = GenDocumento.objects.filter(
            documento_tipo_id=1, estado_aprobado=True, fecha_vence__lt=fecha_actual
            ).aggregate(cantidad=Count('id'), saldo_pendiente=Sum('pendiente'))
        resumen['saldo_pendiente'] = resumen['saldo_pendiente'] or 0
        resumen_vigente['saldo_pendiente'] = resumen_vigente['saldo_pendiente'] or 0
        resumen_vencido['saldo_pendiente'] = resumen_vencido['saldo_pendiente'] or 0
        return Response({'resumen': resumen, 'resumen_vigente': resumen_vigente, 'resumen_vencido': resumen_vencido}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path=r'resumen-pagar',)
    def resumen_pagar(self, request):      
        fecha_actual = timezone.now().date()
        resumen = GenDocumento.objects.filter(
            documento_tipo_id=5, estado_aprobado=True
            ).aggregate(cantidad=Count('id'), saldo_pendiente=Sum('pendiente'))
        resumen_vigente = GenDocumento.objects.filter(
            documento_tipo_id=5, estado_aprobado=True, fecha_vence__gte=fecha_actual
            ).aggregate(cantidad=Count('id'), saldo_pendiente=Sum('pendiente'))
        resumen_vencido = GenDocumento.objects.filter(
            documento_tipo_id=5, estado_aprobado=True, fecha_vence__lt=fecha_actual
            ).aggregate(cantidad=Count('id'), saldo_pendiente=Sum('pendiente'))
        resumen['saldo_pendiente'] = resumen['saldo_pendiente'] or 0
        resumen_vigente['saldo_pendiente'] = resumen_vigente['saldo_pendiente'] or 0
        resumen_vencido['saldo_pendiente'] = resumen_vencido['saldo_pendiente'] or 0
        return Response({'resumen': resumen, 'resumen_vigente': resumen_vigente, 'resumen_vencido': resumen_vencido}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path=r'resumen-venta-dia',)
    def resumen_venta_dia(self, request):      
        fecha_actual = timezone.now().date()
        # Obtener el primer y último día del mes actual
        primer_dia_mes = fecha_actual.replace(day=1)
        ultimo_dia_mes = (primer_dia_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        dias_del_mes = [primer_dia_mes + timedelta(days=i) for i in range((ultimo_dia_mes - primer_dia_mes).days + 1)]
        ventas_por_dia = GenDocumento.objects.filter(fecha__year=fecha_actual.year, fecha__month=fecha_actual.month
                                                  ).annotate(dia=TruncDay('fecha')
                                                             ).values('dia'
                                                                      ).annotate(total=Sum('total')).order_by('dia')
        ventas_dict = {venta['dia']: venta['total'] for venta in ventas_por_dia}
        venta_dia = [{'dia': dia, 'total': ventas_dict.get(dia, 0)} for dia in dias_del_mes]        
        return Response({'resumen': venta_dia}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path=r'importar-detalle',)
    def importar_detalle(self, request):
        raw = request.data
        documento_id = raw.get('documento_id')
        archivo_base64 = raw.get('archivo_base64')
        if documento_id and archivo_base64:
            try:
                documento = GenDocumento.objects.get(pk=documento_id)
            except GenDocumento.DoesNotExist:
                return Response({'mensaje':'El documento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
            try:
                archivo_data = base64.b64decode(archivo_base64)
                archivo = BytesIO(archivo_data)
                wb = openpyxl.load_workbook(archivo)
                sheet = wb.active         
            except Exception as e:     
                return Response({'mensaje':'Error procesando el archivo', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)  
            
            data_documento_detalle = []
            errores = False
            errores_datos = []
            registros_importados = 0
            if documento.documento_tipo_id == 13:
                for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                    if len(row) == 5:
                        data = {
                            'cuenta': row[0],
                            'numero_identificacion':row[1],
                            'debito': row[2] if row[2] is not None else 0,
                            'credito': row[3] if row[3] is not None else 0,
                            'base': row[4] if row[4] is not None else 0,
                            'descripcion': row[5]                    
                        }                    
                        if not data['cuenta']:
                            error_dato = {
                                'fila': i,
                                'Mensaje': 'Debe digitar la cuenta'
                            }
                            errores_datos.append(error_dato)
                            errores = True
                        else:
                            cuenta = ConCuenta.objects.filter(codigo=data['cuenta']).first()
                            if cuenta is None:
                                error_dato = {
                                    'fila': i,
                                    'Mensaje': f'La cuenta {data["cuenta"]} no existe'
                                }
                                errores_datos.append(error_dato)
                                errores = True
                            else:
                                data['cuenta_id'] = cuenta.id

                        if not data['numero_identificacion']:
                            error_dato = {
                                'fila': i,
                                'Mensaje': 'Debe digitar el numero de identificacion'
                            }
                            errores_datos.append(error_dato)
                            errores = True  
                        else:
                            contacto = GenContacto.objects.filter(numero_identificacion=data['numero_identificacion']).first()
                            if contacto is None:
                                error_dato = {
                                    'fila': i,
                                    'Mensaje': f'El contacto con numero identificacion {data["numero_identificacion"]} no existe'
                                }
                                errores_datos.append(error_dato)
                                errores = True
                            else:
                                data['contacto_id'] = contacto.id                                 
                        
                        if data['debito'] == 0 and data['credito'] == 0:
                                error_dato = {
                                    'fila': i,
                                    'Mensaje': f'Los debitos y creditos estan en cero'
                                }
                                errores_datos.append(error_dato)
                                errores = True
                        else:
                            if data['debito'] != 0 and data['credito'] != 0:
                                error_dato = {
                                    'fila': i,
                                    'Mensaje': f'Los debitos y creditos tienen valores'
                                }
                                errores_datos.append(error_dato)
                                errores = True
                            else:
                                total = data['debito']
                                naturaleza = 'D'
                                if data['credito'] > 0:
                                    total = data['credito']
                                    naturaleza = 'C'
                                data['naturaleza'] = naturaleza
                                data['total'] = total
                        data_documento_detalle.append(data) 
                    else:
                        error_dato = {
                            'fila': i,
                            'Mensaje': f'La linea no tiene 5 columnas'
                        }
                        errores_datos.append(error_dato)
                        errores = True
            if errores == False:
                for detalle in data_documento_detalle:
                    GenDocumentoDetalle.objects.create(
                        documento=documento,
                        cuenta_id=detalle['cuenta_id'],
                        contacto_id=detalle['contacto_id'],
                        total=detalle['total'],
                        base_impuesto=detalle['base'],
                        naturaleza=detalle['naturaleza'],
                        detalle=detalle['descripcion']
                    )
                    registros_importados += 1
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                return Response({'errores': True, 'errores_datos': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'generar-nomina-electronica',)
    def generar_nomina_electronica(self, request):      
        raw = request.data
        anio = int(raw.get('anio'))
        mes = int(raw.get('mes'))
        if anio and mes:                    
            fecha_desde = date(anio, mes, 1)            
            ultimo_dia_mes = calendar.monthrange(anio, mes)[1]
            fecha_hasta = date(anio, mes, ultimo_dia_mes)
            nominas_mes = GenDocumento.objects.filter(fecha__gte=fecha_desde, 
                                                      fecha__lte=fecha_hasta, 
                                                      documento_tipo_id=14,
                                                      documento_referencia_id = None,
                                                      estado_aprobado = True)\
                                            .values('contacto_id', 'contrato_id')\
                                            .annotate(
                                                base_cotizacion=Sum('base_cotizacion'),
                                                base_prestacion=Sum('base_prestacion'),
                                                deduccion=Sum('deduccion'),
                                                devengado=Sum('devengado'),
                                                total=Sum('total'))           
            for nomina_mes in nominas_mes:
                contrato = HumContrato.objects.get(pk=nomina_mes['contrato_id'])
                data = {
                    'empresa': 1,
                    'documento_tipo': 15,
                    'fecha': fecha_desde,
                    'fecha_contable': fecha_desde,                    
                    'fecha_hasta': fecha_hasta,
                    'contacto': nomina_mes['contacto_id'],
                    'contrato': nomina_mes['contrato_id'],
                    'grupo': contrato.grupo_id,
                    'salario': contrato.salario,
                    'base_cotizacion': nomina_mes['base_cotizacion'],
                    'base_prestacion': nomina_mes['base_prestacion'],
                    'deduccion': nomina_mes['deduccion'],
                    'devengado': nomina_mes['devengado'],
                    'total': nomina_mes['total']
                }
                documento_serializador = GenDocumentoSerializador(data=data)
                if documento_serializador.is_valid():
                    documento = documento_serializador.save()
                    nominas = GenDocumento.objects.filter(fecha__gte=fecha_desde, 
                                                          fecha__lte=fecha_hasta, 
                                                          documento_tipo_id=14,
                                                          contacto_id = nomina_mes['contacto_id'],
                                                          contrato_id = nomina_mes['contrato_id'],
                                                          documento_referencia_id = None,
                                                          estado_aprobado = True) 
                    for nomina in nominas:
                        nomina.documento_referencia = documento
                        nomina.save() 

                else:
                    return Response({'validaciones':documento_serializador.errors}, status=status.HTTP_400_BAD_REQUEST) 
            return Response({'resumen': 1}, status=status.HTTP_200_OK)

        else:
            return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)           

    @staticmethod
    def notificar(documento_id):
        try:
            documento = GenDocumento.objects.get(id=documento_id)
            if documento.estado_electronico_notificado == False:
                if documento.documento_tipo.documento_clase_id in [100, 101, 102]:
                    configuracion = GenConfiguracion.objects.select_related('formato_factura').filter(empresa_id=1).values().first()
                    documentoGenerar = DocumentoViewSet.consulta_imprimir(documento_id)
                    formatoFactura = FormatoFactura()
                    pdf = formatoFactura.generar_pdf(documentoGenerar, configuracion)   
                    pdf_base64 = "data:application/pdf;base64," + base64.b64encode(pdf).decode('utf-8')            
                    wolframio = Wolframio()
                    respuesta = wolframio.notificar(documento.electronico_id, pdf_base64)
                    if respuesta['error'] == False: 
                        documento.estado_electronico_notificado = True                
                        documento.save()     
                    return respuesta                        
                else:
                    documento.estado_electronico_notificado = True                
                    documento.save()
                    return {'error':False}
            else:  
                return {'error':True, 'mensaje':'El documento ya fue notificado con anterioridad pruebe re-notificando'}
        except GenDocumento.DoesNotExist:
            return {'error':True, 'mensaje':'El documento no existe'}
        
    @staticmethod
    def consulta_imprimir(codigoDocumento):
        documento = GenDocumento.objects.select_related('empresa', 'documento_tipo', 'contacto', 'resolucion', 'metodo_pago', 'contacto__ciudad', 'empresa__tipo_persona', 'documento_referencia', 'plazo_pago').filter(id=codigoDocumento).values(
            'id', 'fecha', 'fecha_validacion', 'fecha_vence', 'numero', 'soporte', 'qr', 'cue', 'resolucion_id', 'contacto_id',
            'subtotal', 'total', 'comentario', 'orden_compra', 'metodo_pago__nombre',
            'contacto__nombre_corto', 'contacto__correo', 'contacto__telefono', 'contacto__numero_identificacion', 'contacto__direccion', 
            'contacto__ciudad__nombre', 
            'empresa__tipo_persona__nombre', 'empresa__numero_identificacion', 'empresa__digito_verificacion', 'empresa__direccion', 'empresa__telefono',
            'empresa__nombre_corto', 'empresa__imagen', 'empresa__ciudad__nombre', 'documento_tipo__nombre', 'resolucion__prefijo',
            'resolucion__consecutivo_desde', 'resolucion__consecutivo_hasta', 'resolucion__numero', 'resolucion__fecha_hasta',
            'documento_referencia__numero', 'documento_tipo__documento_clase_id', 'plazo_pago__nombre'
        ).first()

        # Obtener los detalles del documento
        documentoDetalles = GenDocumentoDetalle.objects.filter(documento_id=documento['id']).values('id', 'cantidad', 'precio', 'descuento', 'total','item__nombre', 'item_id')

        # Obtener los IDs de los detalles del documento
        ids_documentodetalles = list(documentoDetalles.values_list('id', flat=True))

        # Filtrar los DocumentoImpuesto que están asociados a los detalles del documento
        documentoImpuestos = GenDocumentoImpuesto.objects.filter(documento_detalle__in=ids_documentodetalles).values(
        'id',
        'total',
        'impuesto__nombre',
        'impuesto__nombre_extendido',
        'impuesto_id',
        'documento_detalle_id'
        )

        # Agregar los detalles al diccionario documento
        documento['documento_detalles'] = list(documentoDetalles)
        documento['documento_impuestos'] = list(documentoImpuestos)

        return documento
    
    @staticmethod
    def validacion_aprobar(documento_id, consecutivo):
        try:
            documento = GenDocumento.objects.get(id=documento_id)
            fecha = date.today()
            if documento.estado_aprobado == False:
                if documento.documento_tipo.documento_clase_id in (100,303):
                    documento_detalle = GenDocumentoDetalle.objects.filter(documento=documento)
                    if documento_detalle or documento.documento_tipo_id == 15:
                        if documento.resolucion:
                            if isinstance(documento.resolucion.fecha_hasta, date):
                                if documento.resolucion.fecha_hasta <= fecha:
                                    return {'error':True, 'mensaje':'La fecha de la resolucion esta vencida', 'codigo':1}
                            if consecutivo < documento.resolucion.consecutivo_desde or consecutivo > documento.resolucion.consecutivo_hasta:
                                return {'error':True, 'mensaje':f'El consecutivo {consecutivo} no corresponde con la resolucion desde {documento.resolucion.consecutivo_desde} hasta {documento.resolucion.consecutivo_hasta}', 'codigo':1}
                    else:
                        return {'error':True, 'mensaje':'El documento no tiene detalles', 'codigo':1} 

                if documento.documento_tipo.documento_clase_id == 200:
                    resultado = (
                        GenDocumentoDetalle.objects
                        .filter(documento_id=documento_id)
                        .exclude(documento_afectado_id__isnull=True)
                        .values('documento_afectado_id')
                        .annotate(
                            total_pago=Sum('pago'),
                            pendiente=F('documento_afectado__pendiente')))                        
                    for entrada in resultado:
                        if entrada['pendiente'] < entrada['total_pago']:
                            return {'error':True, 'mensaje':f"El documento {entrada['documento_afectado_id']} tiene saldo pendiente {entrada['pendiente']} y se va afectar {entrada['total_pago']}", 'codigo':1}                            
                    #result_list = list(resultado)
                    #print(result_list)
                
                if documento.documento_tipo.documento_clase_id == 702:
                    if documento.contacto.nombre1 and documento.contacto.apellido1:
                        pass
                    else:                        
                        return {'error':True, 'mensaje':'El contacto no tiene nombre1 o apellido1', 'codigo':1}
                return {'error':False}                    
            else:
                return {'error':True, 'mensaje':'El documento ya esta aprobado', 'codigo':1}        
        except GenDocumento.DoesNotExist:
            return {'error':True, 'mensaje':'El documento no existe'}
        
    @staticmethod
    def validacion_anular(documento_id):
        try:
            documento = GenDocumento.objects.get(id=documento_id)
            if documento.documento_tipo_id == 1:                
                if documento.estado_anulado == False:    
                    if documento.estado_aprobado == True:
                        if documento.estado_electronico_enviado == False:
                            if documento.afectado <= 0:
                                #documento_detalle = DocumentoDetalle.objects.filter(documento=documento)
                                return {'error':False}                    
                            else:
                                return {'error':True, 'mensaje':'El documento esta afectado, no se puede anular', 'codigo':1}
                        else:
                            return {'error':True, 'mensaje':'Los documentos electronicos enviados a la DIAN no se pueden anular', 'codigo':1}
                    else:
                        return {'error':True, 'mensaje':'El documento debe estar aprobado', 'codigo':1}
                else:
                    return {'error':True, 'mensaje':'El documento ya esta anulado', 'codigo':1}        
            else:
                return {'error':True, 'mensaje':'El tipo de documento no se puede anular'}            
        except GenDocumento.DoesNotExist:
            return {'error':True, 'mensaje':'El documento no existe'}        
    

