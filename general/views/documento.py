from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from general.models.documento import Documento
from general.models.documento_detalle import DocumentoDetalle
from general.models.documento_impuesto import DocumentoImpuesto
from general.models.empresa import Empresa
from general.models.resolucion import Resolucion
from general.serializers.documento import DocumentoSerializador, DocumentoRetrieveSerializador
from general.serializers.documento_detalle import DocumentoDetalleSerializador
from general.serializers.documento_impuesto import DocumentoImpuestoSerializador
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
import locale
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from decouple import config
from .kiai import enviar_software_estrategico

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
            documento = documentoSerializador.save()            
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
                        documentoEliminar.delete()   
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
                documento.estado_aprobado = True
                documento.save()
                return Response({'estado_aprobado': True}, status=status.HTTP_200_OK)
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

        try:
            documento = Documento.objects.get(pk=codigoDocumento)
            contacto = documento.contacto
            documentoDetalles = DocumentoDetalle.objects.filter(documento_id=codigoDocumento)
            empresa = Empresa.objects.get(pk=documento.empresa.id)
            documentoImpuestos = DocumentoImpuesto.objects.filter(documento_detalle__in=documentoDetalles)
            resolucion = None
            if documento.resolucion_id is not None:
                resolucion = Resolucion.objects.get(pk=documento.resolucion.id)
        except Documento.DoesNotExist:
            pass

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="hello.pdf"'
        p = canvas.Canvas(response, pagesize=letter)

        try:
            locale.setlocale(locale.LC_ALL, 'es_CO.utf8')
        except locale.Error:
            pass

        stylesheet = getSampleStyleSheet()
        normalStyle = stylesheet['Normal']

        paragraph = Paragraph("El pago se realizará en un plazo de tres meses desde la emisión de esta factura, se realizará mediante transferencia bancaria.", normalStyle)

        def draw_header():

            region = config('DO_REGION')
            bucket = config('DO_BUCKET')

            imagen_defecto_url = 'https://itrio.fra1.cdn.digitaloceanspaces.com/test/empresa/logo_defecto.jpg'

            # Intenta cargar la imagen desde la URL

            logo_url = f'https://{region}.{bucket}.cdn.digitaloceanspaces.com/{empresa.imagen}'
            try:
                logo = ImageReader(logo_url)
            except Exception as e:
                # Si se produce un error, establece la URL en la imagen de defecto
                logo_url = imagen_defecto_url
                logo = ImageReader(logo_url)

            tamano_cuadrado = 1 * inch
            coord_x = 50
            coord_y = 680
            p.drawImage(logo, coord_x, coord_y, width=tamano_cuadrado, height=tamano_cuadrado, mask='auto')

            #Emisor
            p.setFont("Helvetica", 10)
            p.drawString(250, 740, empresa.nombre_corto if empresa.nombre_corto else "")
            p.drawString(250, 726, empresa.numero_identificacion if empresa.numero_identificacion else "")
            p.drawString(250, 712, empresa.direccion if empresa.direccion else "")
            p.drawString(250, 698, empresa.telefono if empresa.telefono else "")
            p.setFont("Helvetica-Bold", 11.5)
            p.drawRightString(550, 690, f"FACTURA N°: {documento.numero}")
            p.setFont("Helvetica", 10)
            p.drawRightString(550, 676, f"Fecha: {documento.fecha}")
            p.setFont("Helvetica-Bold", 10)

            #Cliente
            p.drawString(50, 665, "Datos cliente")
            p.setFont("Helvetica", 10)
            nombre_corto = getattr(contacto, 'nombre_corto', 'Vacio' if not contacto else '')
            p.drawString(50, 650, str(nombre_corto))
            p.drawString(50, 636, str(contacto.direccion))
            p.drawString(50, 622, str(contacto.ciudad.nombre))
            p.drawString(50, 608, str(contacto.correo))
            p.drawString(50, 594, str(contacto.telefono))

            #resolución
            if resolucion:
                texto_resolucion = f"FACTURA ELECTRÓNICA DE VENTA No. {resolucion.prefijo} {documento.numero}"
            else:
                texto_resolucion = f"FACTURA ELECTRÓNICA DE VENTA No. {documento.numero}"
            p.drawRightString(550, 622, texto_resolucion)
            # p.drawRightString(550, 622, f"FACTURA ELECTRÓNICA DE VENTA No. {resolucion.prefijo} {documento.numero}")
            #Linea separadora
            p.setStrokeColorRGB(200/255, 200/255, 200/255)
            p.line(50, 580, 550, 580)
            p.setStrokeColorRGB(0, 0, 0)

            #Encabezado detalles
            p.setFont("Helvetica-Bold", 10)
            p.drawString(60, 555, "Descripción / Producto")
            p.drawString(250, 555, "Impuestos")
            p.drawString(310, 555, "Cantidad")
            p.drawString(380, 555, "Desc")
            p.drawString(440, 555, "Subtotal")
            p.drawString(520, 555, "Total")
            p.setFont("Helvetica", 10)

        def draw_totals(p, y):
            #dejo el llamado de y en caso de que se requiera que se construya de manera dinamica
            #Linea separadora
            p.setStrokeColorRGB(200/255, 200/255, 200/255)
            p.line(400, 215, 550, 215)
            p.setStrokeColorRGB(0, 0, 0)

            #Bloque totales
            p.setFont("Helvetica-Bold", 10)
            p.drawString(400, 200, "Subtotal")
            p.drawRightString(550, 200, f"${locale.format_string('%d', int(documento.subtotal), grouping=True)}")
            
            # Crear un diccionario para almacenar los totales por impuesto_id y su nombre
            impuesto_totals = {}

            # Recorrer los objetos DocumentoImpuesto
            for impuesto in documentoImpuestos:
                impuesto_id = impuesto.impuesto.id  # ID del impuesto
                nombre_impuesto = impuesto.impuesto.nombre_extendido  # Nombre del impuesto
                total = impuesto.total

                # Verificar si el impuesto_id ya existe en el diccionario
                if impuesto_id in impuesto_totals:
                    # Si existe, sumar el total al valor existente
                    impuesto_totals[impuesto_id]['total'] += total
                else:
                    # Si no existe, crear una nueva entrada en el diccionario con el total y el nombre del impuesto
                    impuesto_totals[impuesto_id] = {'total': total, 'nombre': nombre_impuesto}

            # Definir la posición "y" inicial
            y = 180

            # Recorrer el diccionario de totales de impuestos
            for impuesto_id, data in impuesto_totals.items():
                nombre_impuesto = data['nombre']
                total_acumulado = data['total']
                
                p.drawString(400, y, nombre_impuesto)
                p.drawRightString(550, y, f"${locale.format_string('%d', int(total_acumulado), grouping=True)}")
                y -= 20

            p.drawString(400, y, "Total general")
            p.drawRightString(550, y, f"${locale.format_string('%d', int(documento.total), grouping=True)}")

            #Comentario
            paragraph.wrapOn(p, 280, 400)
            paragraph.drawOn(p, 50, 180)

        y = 520
        page_number = 1
        detalles_en_pagina = 0

        draw_header()

        for index, detalle in enumerate(documentoDetalles):
            impuestos_detalle = documentoImpuestos.filter(documento_detalle_id=detalle.id)
            impuestos_unicos = []
            # Iterar sobre los impuestos relacionados con el detalle actual
            for impuesto_detalle in impuestos_detalle:
                nombre_impuesto = impuesto_detalle.impuesto.nombre
                
                # Si el nombre del impuesto no está en la lista de impuestos únicos, agrégalo
                if nombre_impuesto not in impuestos_unicos:
                    impuestos_unicos.append(nombre_impuesto)

                # Ahora, puedes imprimir los nombres de impuestos únicos en una línea
                impuestos_str = ', '.join(impuestos_unicos)

            p.setStrokeColorRGB(200/255, 200/255, 200/255)
            p.line(50, y + 15, 550, y + 15)
            p.setStrokeColorRGB(0, 0, 0)
            p.drawString(60, y, str(detalle.item.nombre[:30]))
            p.drawString(250, y, impuestos_str)
            p.drawRightString(350, y, str(int(detalle.cantidad)))
            p.drawRightString(400, y, str(int(detalle.porcentaje_descuento)))
            p.drawRightString(480, y, f"${locale.format_string('%d', int(detalle.subtotal), grouping=True)}")
            p.drawRightString(550, y, f"${locale.format_string('%d', int(detalle.total), grouping=True)}")
            y -= 30
            detalles_en_pagina += 1

            if detalles_en_pagina == 10 or index == len(documentoDetalles) - 1:
                draw_totals(p, y)

                if index != len(documentoDetalles) - 1:
                    p.showPage()
                    page_number += 1
                    y = 520
                    draw_header()
                    detalles_en_pagina = 0

        p.save()
        return response

    
    @staticmethod
    def listar(desplazar, limite, limiteTotal, filtros, ordenamientos):
        documentos = Documento.objects.all()
        if filtros:
            for filtro in filtros:
                documentos = documentos.filter(**{filtro['propiedad']: filtro['valor_1']})
        if ordenamientos:
            documentos = documentos.order_by(*ordenamientos)              
        documentos = documentos[desplazar:limite+desplazar]
        itemsCantidad = Documento.objects.all()[:limiteTotal].count()
        serializador = DocumentoSerializador(documentos, many=True) 
        campos = []
        camposSerializador = DocumentoSerializador().get_fields()
        for nombre, field_instance in camposSerializador.items():
            tipo = field_instance.__class__.__name__
            etiqueta = field_instance.label or nombre
            campos.append({"nombre": nombre, "tipo": tipo, "etiqueta": etiqueta}) 
          
        respuesta = {'propiedades': campos, 'registros': serializador.data, "cantidad_registros": itemsCantidad}
        return respuesta
    
    @action(detail=False, methods=["post"], url_path=r'emitir',)
    def emitir(self, request):
        try:
            raw = request.data
            codigoDocumento = raw.get('documento_id')
            if codigoDocumento:
                documento = Documento.objects.get(pk=codigoDocumento)
                if documento.estado_aprobado == True:
                    empresa = Empresa.objects.get(pk=1)

                    #Se construye el obejto inicial

                    datos_factura = {
                        'dat_suscriptor' : empresa.suscriptor,
                        'dat_nitFacturador': empresa.numero_identificacion,
                        'dat_claveTecnica' : documento.resolucion.clave_tecnica,
                        'dat_setPruebas' : documento.resolucion.set_prueba,
                        'dat_tipoAmbiente' : documento.resolucion.ambiente,
                        'res_numero' : documento.resolucion.numero,
                        'res_prefijo' : documento.resolucion.prefijo,
                        'res_fechaDesde' : documento.resolucion.fecha_desde,
                        'res_fechaHasta' : documento.resolucion.fecha_hasta,
                        'res_desde' : documento.resolucion.consecutivo_desde,
                        'res_hasta' : documento.resolucion.consecutivo_hasta,
                        'doc_codigo' : codigoDocumento,
                        'doc_tipo' : documento.documento_tipo.documento_clase.codigo_dian,
                        'doc_tipo_operacion' : 10,
                        'doc_codigoDocumento' : '',
                        'doc_formaPago' : documento.metodo_pago.id,
                        'doc_comentarios' : '',
                        'doc_cue' : '',
                        'doc_prefijo' : '',
                        'doc_numero' : documento.numero,
                        'doc_fecha' : documento.fecha,
                        'doc_fecha_vence' : documento.fecha_vence,
                        'doc_orden_compra' : '',
                        'doc_hora' : '12:00:00-05:00',
                        'doc_hora2' : '12:00:00',
                        'doc_subtotal' : float(documento.subtotal),
                        'doc_baseIva' : float(documento.base_impuesto),
                        'doc_iva' : 0,
                        'doc_inc' : 0,
                        'doc_ica' : 0,
                        'doc_total' : float(documento.total),
                        'ref_cue' : '',
                        'ref_codigoExterno' : '',
                        'ref_numero' : '18760000001',
                        'ref_prefijo' : '',
                        'ref_fecha' : '',
                        'em_tipoPersona' : empresa.tipo_persona.id,
                        'em_numeroIdentificacion' : empresa.numero_identificacion,
                        'em_digitoVerificacion' : empresa.digito_verificacion,
                        'em_nombreCompleto' : empresa.nombre_corto,
                        'em_matriculaMercantil' : '',
                        'em_codigoCiudad' : empresa.ciudad.codigo_postal,
                        'em_nombreCiudad' : empresa.ciudad.nombre,
                        'em_codigoPostal' : empresa.ciudad.codigo_postal,
                        'em_codigoDepartamento' : empresa.ciudad.estado.codigo,
                        'em_nombreDepartamento' : empresa.ciudad.estado.nombre,
                        'em_correo' : empresa.correo,
                        'em_direccion' : empresa.direccion,
                        'ad_tipoIdentificacion' : documento.contacto.identificacion.codigo,
                        'ad_numeroIdentificacion' : documento.contacto.numero_identificacion,
                        'ad_digitoVerificacion' : documento.contacto.digito_verificacion,
                        'ad_nombreCompleto' : documento.contacto.nombre_corto,
                        'ad_tipoPersona' : documento.contacto.tipo_persona.id,
                        'ad_regimen' : documento.contacto.regimen.id,
                        'ad_responsabilidadFiscal' : '',
                        'ad_direccion' : documento.contacto.direccion,
                        'ad_barrio' : documento.contacto.barrio,
                        'ad_codigoPostal' : documento.contacto.ciudad.codigo_postal,
                        'ad_telefono' : documento.contacto.telefono,
                        'ad_correo' : documento.contacto.correo,
                        'ad_codigoCIUU' : documento.contacto.codigo_ciuu,
                        'ad_codigoCiudad' : documento.contacto.ciudad.codigo_postal,
                        'ad_nombreCiudad' : documento.contacto.ciudad.nombre,
                        'ad_codigoDepartamento' : documento.contacto.ciudad.estado.codigo,
                        'ad_nombreDepartamento' : documento.contacto.ciudad.estado.nombre,
                    }

                    arr_item = []
                    cantidad_items = 0
                    documentoDetalles = DocumentoDetalle.objects.filter(documento=codigoDocumento)
                    for documentoDetalle in documentoDetalles:
                        cantidad_items += 1
                        arr_item.append({
                            "item_id": cantidad_items,
                            "item_codigo": documentoDetalle.pk,
                            "item_nombre": documentoDetalle.item.nombre,
                            "item_cantidad": float(documentoDetalle.cantidad),
                            "item_precio": float(documentoDetalle.precio),
                            "item_subtotal": float(documentoDetalle.subtotal),
                            "item_base_iva": float(0),
                            "item_iva": float(0),
                            "item_porcentaje_iva": float(0)
                        })

                    datos_factura['doc_itemes'] = arr_item
                    datos_factura['doc_cantidad_item'] = cantidad_items

                    proceso_factura_electronica = enviar_software_estrategico(datos_factura)


                    # Verificar si la solicitud fue exitosa (código de respuesta 200)
                    # if response.status_code == 200:
                    #     # Procesar la respuesta de la API aquí
                    #     data = response.json()  # Suponiendo que la API responde en formato JSON
                    #     # ...

                    #     # Guardar el documento u realizar otras acciones necesarias
                    #     documento.save()
                    # else:
                    #     return Response({'mensaje': 'La API externa respondió con un error', 'codigo': 2}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({'mensaje': 'El documento no se puede emitir ya que no está aprobado', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
        except Documento.DoesNotExist:
            return Response({'mensaje': 'El documento no existe', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)