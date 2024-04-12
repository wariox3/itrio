from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from general.models.documento import Documento
from general.models.documento_detalle import DocumentoDetalle
from general.models.documento_impuesto import DocumentoImpuesto
from general.models.documento_tipo import DocumentoTipo
from general.models.empresa import Empresa
from general.models.resolucion import Resolucion
from general.serializers.documento import DocumentoSerializador, DocumentoRetrieveSerializador
from general.serializers.documento_detalle import DocumentoDetalleSerializador
from general.serializers.documento_impuesto import DocumentoImpuestoSerializador
from general.formatos.factura import FormatoFactura
from general.formatos.cuenta_cobro import FormatoCuentaCobro
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from openpyxl import Workbook
from decouple import config
from datetime import datetime
import base64
from utilidades.wolframio import Wolframio
import json


class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializador
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        pass

    def create(self, request):
        raw = request.data
        documentoSerializador = DocumentoSerializador(data=raw)
        if documentoSerializador.is_valid():
            # Extraemos el tipo de documento
            documento_tipo = documentoSerializador.validated_data['documento_tipo']

            # Aquí debes buscar la resolución asociada al tipo de documento
            # Supongamos que obtienes la resolución asociada al tipo de documento
            resolucion = documento_tipo.resolucion

            # Asignamos la resolución al documento antes de guardarlo
            documento = documentoSerializador.save(resolucion=resolucion)            
            detalles = raw.get('detalles')
            if detalles is not None:
                for detalle in detalles:                
                    detalle['documento'] = documento.id
                    detalleSerializador = DocumentoDetalleSerializador(data=detalle)
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
                                    "total":impuesto['total']
                                }
                                documentoImpuestoSerializador = DocumentoImpuestoSerializador(data=datosDocumentoImpuesto)
                                if documentoImpuestoSerializador.is_valid():
                                    documentoImpuestoSerializador.save()
                                else:
                                    return Response({'mensaje':'Errores de validacion detalle impuesto', 'codigo':14, 'validaciones': documentoImpuestoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                                
                    else:
                        return Response({'mensaje':'Errores de validacion detalle', 'codigo':14, 'validaciones': detalleSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)            
                documentoDetalles = DocumentoDetalle.objects.filter(documento=documento.id)
                documentoDetallesSerializador = DocumentoDetalleSerializador(documentoDetalles, many=True)
                detalles = documentoDetallesSerializador.data
                for detalle in detalles:
                    documentoImpuestos = DocumentoImpuesto.objects.filter(documento_detalle=detalle['id'])
                    documentoImpuestosSerializador = DocumentoImpuestoSerializador(documentoImpuestos, many=True)
                    detalle['impuestos'] = documentoImpuestosSerializador.data
                documentoRespuesta = documentoSerializador.data
                documentoRespuesta['detalles'] = detalles
                return Response({'documento': documentoRespuesta}, status=status.HTTP_200_OK)
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': documentoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        queryset = Documento.objects.all()
        documento = get_object_or_404(queryset, pk=pk)
        documentoSerializador = DocumentoRetrieveSerializador(documento)
        documentoDetalles = DocumentoDetalle.objects.filter(documento=pk)
        documentoDetallesSerializador = DocumentoDetalleSerializador(documentoDetalles, many=True)
        detalles = documentoDetallesSerializador.data
        for detalle in detalles:
            documentoImpuestos = DocumentoImpuesto.objects.filter(documento_detalle=detalle['id'])
            documentoImpuestosSerializador = DocumentoImpuestoSerializador(documentoImpuestos, many=True)
            detalle['impuestos'] = documentoImpuestosSerializador.data
        documentoRespuesta = documentoSerializador.data
        documentoRespuesta['detalles'] = detalles
        return Response({'documento':documentoRespuesta}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        raw = request.data
        documento = Documento.objects.get(pk=pk)
        documentoSerializador = DocumentoSerializador(documento, data=raw, partial=True)
        if documentoSerializador.is_valid():
            documentoSerializador.save()
            detalles = raw.get('detalles')
            if detalles is not None:
                for detalle in detalles:                
                    if detalle.get('id'):
                        documentoDetalle = DocumentoDetalle.objects.get(pk=detalle['id'])
                        detalleSerializador = DocumentoDetalleSerializador(documentoDetalle, data=detalle, partial=True)    
                    else:
                        detalle['documento'] = documento.id
                        detalleSerializador = DocumentoDetalleSerializador(data=detalle)
                    if detalleSerializador.is_valid():
                        documentoDetalle = detalleSerializador.save() 
                        impuestos = detalle.get('impuestos')
                        if impuestos is not None:
                            for impuesto in impuestos:
                                if impuesto.get('id'):
                                    documentoImpuesto = DocumentoImpuesto.objects.get(pk=impuesto['id'])
                                    documentoImpuestoSerializador = DocumentoImpuestoSerializador(documentoImpuesto, data=impuesto, partial=True)    
                                else:        
                                    impuesto['documento_detalle'] = documentoDetalle.id                                     
                                    documentoImpuestoSerializador = DocumentoImpuestoSerializador(data=impuesto)                            
                                if documentoImpuestoSerializador.is_valid():
                                    documentoImpuestoSerializador.save()
                                else:
                                    return Response({'mensaje':'Errores de validacion detalle impuesto', 'codigo':14, 'validaciones': documentoImpuestoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                                                        
                        impuestosEliminados = detalle.get('impuestos_eliminados')
                        if impuestosEliminados is not None:
                            for documentoImpuesto in impuestosEliminados:                                
                                documentoImpuesto = DocumentoImpuesto.objects.get(pk=documentoImpuesto)
                                documentoImpuesto.delete()                         
                    else:
                        return Response({'mensaje':'Errores de validacion detalle', 'codigo':14, 'validaciones': detalleSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)            
            detallesEliminados = raw.get('detalles_eliminados')
            if detallesEliminados is not None:
                for detalle in detallesEliminados:                                
                    documentoDetalle = DocumentoDetalle.objects.get(pk=detalle)
                    documentoDetalle.delete()
            documentoDetalles = DocumentoDetalle.objects.filter(documento=pk)
            documentoDetallesSerializador = DocumentoDetalleSerializador(documentoDetalles, many=True)
            detalles = documentoDetallesSerializador.data
            for detalle in detalles:
                documentoImpuestos = DocumentoImpuesto.objects.filter(documento_detalle=detalle['id'])
                documentoImpuestosSerializador = DocumentoImpuestoSerializador(documentoImpuestos, many=True)
                detalle['impuestos'] = documentoImpuestosSerializador.data
            documentoRespuesta = documentoSerializador.data
            documentoRespuesta['detalles'] = detalles                   
            return Response({'documento': documentoRespuesta}, status=status.HTTP_200_OK)                    
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': documentoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'lista',)
    def lista(self, request):
        raw = request.data
        codigoDocumentoTipo = raw.get('documento_tipo_id')
        if codigoDocumentoTipo:
            desplazar = raw.get('desplazar', 0)
            limite = raw.get('limite', 50)    
            limiteTotal = raw.get('limite_total', 5000)                
            filtros = raw.get('filtros')
            ordenamientos = raw.get('ordenamientos')                                     
            respuesta = DocumentoViewSet.listar(desplazar, limite, limiteTotal, filtros, ordenamientos)     
            return Response(respuesta, status=status.HTTP_200_OK)
        return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'eliminar',)
    def eliminar(self, request):
        try:
            raw = request.data
            documentos = raw.get('documentos')
            if documentos:  
                for documento in documentos:
                    documentoEliminar = Documento.objects.get(pk=documento)  
                    if documentoEliminar:
                        if documentoEliminar.estado_aprobado == False:
                            documentoEliminar.delete()   
                        else:
                            return Response({'mensaje':'El documento con id ' + str(documentoEliminar.id) + ' no se puede eliminar por que se encuentra aprobado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'mensaje':'Registros eliminados'}, status=status.HTTP_200_OK)
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except Documento.DoesNotExist:
            return Response({'mensaje':'El documento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'aprobar',)
    def aprobar(self, request):
        try:
            raw = request.data
            codigoDocumento = raw.get('id')
            if codigoDocumento:
                documento = Documento.objects.get(pk=codigoDocumento)
                if documento.estado_aprobado == False:                
                    documentoTipo = DocumentoTipo.objects.get(pk=1)
                    if documento.numero is None:
                        documento.numero = documentoTipo.consecutivo
                        documentoTipo.consecutivo += 1
                        documentoTipo.save()                
                    documento.estado_aprobado = True
                    documento.save()
                    return Response({'estado_aprobado': True}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'El documento ya esta aprobado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except Documento.DoesNotExist:
            return Response({'mensaje':'El documento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'excel',)
    def excel(self, request):
        raw = request.data
        desplazar = raw.get('desplazar', 0)
        limite = raw.get('limite', 50)    
        limiteTotal = raw.get('limite_total', 5000)                
        filtros = raw.get('filtros')
        ordenamientos = raw.get('ordenamientos')  
        respuesta = DocumentoViewSet.listar(desplazar, limite, limiteTotal, filtros, ordenamientos)
        
        # Crear un libro de Excel y una hoja
        wb = Workbook()
        ws = wb.active

        # Agregar encabezados de columna
        field_names = [field for field in DocumentoSerializador().get_fields()]
        ws.append(field_names)

        # Agregar datos al archivo Excel
        for row in respuesta['registros']:
            row_data = [row[field] for field in field_names]
            ws.append(row_data)

        # Crear el archivo Excel en memoria
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=documentos.xlsx'
        wb.save(response)
        return response          
    
    @action(detail=False, methods=["post"], url_path=r'imprimir',)
    def imprimir(self, request):
        raw = request.data
        codigoDocumento = raw.get('documento_id')
        documento = self.consulta_imprimir(codigoDocumento)
        #formatoCuentaCobro = FormatoCuentaCobro()
        #pdf = formatoCuentaCobro.generar_pdf(documento)
        formatoFactura = FormatoFactura()
        pdf = formatoFactura.generar_pdf(documento)    
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="factura.pdf"'    
        return response

    @action(detail=False, methods=["post"], url_path=r'emitir',)
    def emitir(self, request):
        try:
            if config('ENV') == "prod":
                raw = request.data
                codigoDocumento = raw.get('documento_id')
                if codigoDocumento:
                    documento = Documento.objects.get(pk=codigoDocumento)
                    if documento.estado_aprobado == True:
                        empresa = Empresa.objects.get(pk=1)
                        if empresa.rededoc_id:
                            if documento.resolucion: 
                                if documento.numero: 
                                    if documento.estado_electronico_enviado == False:                                   
                                        datos_factura = {
                                            "cuentaId": empresa.rededoc_id,
                                            "documentoClaseId" : 1,
                                            "documentoClienteId": documento.id,
                                            "documento" : {
                                                "ambiente" : 1,
                                                "prefijo" : documento.resolucion.prefijo,
                                                "numero" : documento.numero,
                                                "fecha" : str(documento.fecha),
                                                "hora" : str("12:00:00-05:00"),
                                                "fecha_vence" : str(documento.fecha_vence),
                                                "tipo_operacion" : str(10),
                                                "moneda" : "COP",
                                                "resolucion" : str(documento.resolucion.numero),
                                                "forma_pago" : documento.metodo_pago.id,
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

                                        documentoDetalles = DocumentoDetalle.objects.filter(documento=codigoDocumento)
                                        for documentoDetalle in documentoDetalles:
                                            arr_impuestos = []
                                            documentoImpuestoDetalles = DocumentoImpuesto.objects.filter(documento_detalle=documentoDetalle.id)
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
                                                "total_impuestos" : str(documentoImpuestoDetalle.total),
                                                "base" : str(documentoImpuestoDetalle.base),
                                                "subtotal" : str(documentoDetalle.subtotal),
                                                "impuestos" : arr_impuestos
                                            })

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
                                            return Response({'mensaje': 'Documento emitido correctamente', 'codigo': 15}, status=status.HTTP_200_OK)
                                        else:
                                            return Response({'mensaje': respuesta['mensaje'], 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)
                                    else:
                                        return Response({'mensaje': "El documento ya fue enviado", 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)                                        
                                else:
                                    return Response({'mensaje': 'La factura no cuenta con un número', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response({'mensaje': 'La factura no cuenta con una resolución asociada', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
                        else:  
                            return Response({'mensaje': 'La empresa no se encuentra activada para emitir documentos electronicos', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'mensaje': 'El documento no se puede emitir ya que no está aprobado', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje': 'En el entorno de desarrollo no se puede emitir un documento', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)                
        except Documento.DoesNotExist:
            return Response({'mensaje': 'El documento no existe', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path=r'electronico_respuesta_emitir', permission_classes=[permissions.AllowAny])
    def electronico_respuesta(self, request):
        raw = request.data
        documento_id = raw.get('documento_id')
        qr = raw.get('qr')
        cue = raw.get('cue')
        fecha_validacion = raw.get('fecha_validacion')
        if documento_id and qr and cue and fecha_validacion:
            try:
                documento = Documento.objects.get(pk=documento_id)
                if documento.estado_electronico_enviado:
                    fecha_validacion_obj = datetime.strptime(fecha_validacion, '%Y-%m-%d %H:%M:%S')
                    documento.qr = qr
                    documento.cue = cue
                    documento.fecha_validacion = fecha_validacion_obj
                    documento.estado_electronico = True
                    documento.save()                
                    #self.notificar(documento_id)
                    return Response({'respuesta':True}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'No se puede entregar una respuesta porque el documento no se ha enviado'}, status=status.HTTP_400_BAD_REQUEST)
            except Documento.DoesNotExist:
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

    @staticmethod
    def listar(desplazar, limite, limiteTotal, filtros, ordenamientos):
        documentos = Documento.objects.all()
        if filtros:
            for filtro in filtros:
                documentos = documentos.filter(**{filtro['propiedad']: filtro['valor1']})
        if ordenamientos:
            documentos = documentos.order_by(*ordenamientos)              
        documentos = documentos[desplazar:limite+desplazar]
        itemsCantidad = Documento.objects.all()[:limiteTotal].count()
        serializador = DocumentoSerializador(documentos, many=True)           
        respuesta = {'registros': serializador.data, "cantidad_registros": itemsCantidad}
        return respuesta              

    @staticmethod
    def notificar(documento_id):
        try:
            documento = Documento.objects.get(id=documento_id)
            if documento.estado_electronico_notificado == False:
                documentoGenerar = DocumentoViewSet.consulta_imprimir(documento_id)
                formatoFactura = FormatoFactura()
                pdf = formatoFactura.generar_pdf(documentoGenerar)   
                pdf_base64 = "data:application/pdf;base64," + base64.b64encode(pdf).decode('utf-8')            
                wolframio = Wolframio()
                respuesta = wolframio.notificar(documento.electronico_id, pdf_base64)
                if respuesta['error'] == False: 
                    documento.estado_electronico_notificado = True                
                    documento.save()                
                return respuesta
            else:  
                return {'error':True, 'mensaje':'El documento ya fue notificado con anterioridad pruebe re-notificando'}
        except Documento.DoesNotExist:
            return {'error':True, 'mensaje':'El documento no existe'}
        
    @staticmethod
    def consulta_imprimir(codigoDocumento):
        documento = Documento.objects.select_related('empresa', 'documento_tipo', 'contacto', 'resolucion', 'metodo_pago', 'contacto__ciudad', 'empresa__tipo_persona').filter(id=codigoDocumento).values(
            'id',
            'fecha',
            'fecha_validacion',
            'fecha_vence',
            'numero',
            'soporte',
            'qr',
            'cue',
            'resolucion_id',
            'contacto_id',
            'subtotal',
            'total',
            'comentario',
            'metodo_pago__nombre',
            'contacto__nombre_corto',
            'contacto__correo',
            'contacto__telefono',
            'contacto__numero_identificacion',
            'contacto__direccion',
            'contacto__ciudad__nombre',
            'empresa__tipo_persona__nombre',
            'empresa__numero_identificacion',
            'empresa__digito_verificacion',
            'empresa__direccion',
            'empresa__telefono',
            'empresa__nombre_corto',
            'empresa__imagen',
            'empresa__ciudad__nombre',
            'documento_tipo__nombre',
            'resolucion__prefijo',
            'resolucion__consecutivo_desde',
            'resolucion__consecutivo_hasta',
            'resolucion__numero',
            'resolucion__fecha_hasta',
        ).first()

        # Obtener los detalles del documento
        documentoDetalles = DocumentoDetalle.objects.filter(documento_id=documento['id']).values('id', 'cantidad', 'precio', 'descuento', 'total','item__nombre', 'item_id')

        # Obtener los IDs de los detalles del documento
        ids_documentodetalles = list(documentoDetalles.values_list('id', flat=True))

        # Filtrar los DocumentoImpuesto que están asociados a los detalles del documento
        documentoImpuestos = DocumentoImpuesto.objects.filter(documento_detalle__in=ids_documentodetalles).values(
        'id',
        'total',
        'impuesto__nombre',
        'impuesto__nombre_extendido'
        )

        # Agregar los detalles al diccionario documento
        documento['documento_detalles'] = list(documentoDetalles)
        documento['documento_impuestos'] = list(documentoImpuestos)

        return documento