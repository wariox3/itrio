from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from general.models.documento_impuesto import GenDocumentoImpuesto
from general.models.configuracion import GenConfiguracion
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from utilidades.utilidades import convertir_a_letras
from utilidades.utilidades import generar_qr
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.graphics import renderPDF
from decouple import config
import locale
from django.utils.timezone import localtime

class FormatoFactura():

    def generar_pdf(self, id):  
        buffer = BytesIO()   
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setTitle("factura")
        configuracion = GenConfiguracion.objects.select_related('formato_factura').filter(empresa_id=1).values().first()
        documento = GenDocumento.objects.select_related('empresa', 'documento_tipo', 'contacto', 'resolucion', 'metodo_pago', 'contacto__ciudad', 'empresa__tipo_persona', 'documento_referencia', 'plazo_pago').filter(id=id).values(
        'id', 'fecha', 'fecha_validacion', 'fecha_vence', 'numero', 'soporte', 'qr', 'cue', 'resolucion_id', 'contacto_id',
        'subtotal', 'total', 'comentario', 'orden_compra', 'metodo_pago__nombre',
        'contacto__nombre_corto', 'contacto__correo', 'contacto__telefono', 'contacto__numero_identificacion', 'contacto__direccion', 
        'contacto__ciudad__nombre', 
        'empresa__tipo_persona__nombre', 'empresa__numero_identificacion', 'empresa__digito_verificacion', 'empresa__direccion', 'empresa__telefono',
        'empresa__nombre_corto', 'empresa__imagen', 'empresa__ciudad__nombre', 'documento_tipo__nombre', 'resolucion__prefijo',
        'resolucion__consecutivo_desde', 'resolucion__consecutivo_hasta', 'resolucion__numero', 'resolucion__fecha_hasta',
        'documento_referencia__numero', 'documento_tipo__documento_clase_id', 'plazo_pago__nombre'
        ).first()
        estilo_helvetica = ParagraphStyle(name='HelveticaStyle', fontName='Helvetica', fontSize=8, leading=8)
        informacion_factura = configuracion['informacion_factura'] if configuracion['informacion_factura'] else ""
        informacion_factura_con_saltos = informacion_factura.replace('\n', '<br/>')
        informacion_factura_superior = configuracion['informacion_factura_superior'] if configuracion['informacion_factura_superior'] else ""
        informacion_factura_superior_con_saltos = informacion_factura_superior.replace('\n', '<br/>')
        informacion_superior = Paragraph(informacion_factura_superior_con_saltos, estilo_helvetica)
        informacionPago = Paragraph("<b>INFORMACIÓN DE PAGO: </b>" + informacion_factura_con_saltos, estilo_helvetica)
        comentario = Paragraph("<b>COMENTARIOS: </b>" +  str(documento['comentario'] if documento['comentario'] else  ""), estilo_helvetica)

        try:
            locale.setlocale(locale.LC_ALL, 'es_CO.utf8')
        except locale.Error:
            pass


        def draw_header():

            region = config('DO_REGION')
            bucket = config('DO_BUCKET')
            entorno = config('ENV')
            qr = ""
            if documento['qr']:
                qr = documento['qr']
            qr_code_drawing = generar_qr(qr)

            x_pos = 340
            y_pos = 125
            renderPDF.draw(qr_code_drawing, p, x_pos, y_pos)

            imagen_defecto_url = f'https://{bucket}.{region}.digitaloceanspaces.com/itrio/{entorno}/empresa/logo_defecto.jpg'

            # Intenta cargar la imagen desde la URL
            imagen_empresa = documento['empresa__imagen']

            logo_url = f'https://{bucket}.{region}.digitaloceanspaces.com/{imagen_empresa}'
            try:
                logo = ImageReader(logo_url)
            except Exception as e:
                # Si se produce un error, establece la URL en la imagen de defecto
                logo_url = imagen_defecto_url
                logo = ImageReader(logo_url)

            x = 24
            ancho_texto, alto_texto = informacion_superior.wrapOn(p, 480, 500)                        
            y2 = 690 - alto_texto
            informacion_superior.drawOn(p, x+76, y2)
            tamano_cuadrado = 1 * inch
            y = 680
            

            #borde tabla detalles
            p.drawImage(logo, x, y, width=tamano_cuadrado, height=tamano_cuadrado, mask='auto')
            p.setStrokeColorRGB(0.8, 0.8, 0.8)
            #recuadro1
            p.rect(x, 570, 564, 15)
            #recuadro2
            p.rect(x, 240, 564, 330)


            #Emisor
            numero_identificacion = ""
            if documento['empresa__numero_identificacion']:
                numero_identificacion = numero_identificacion+documento['empresa__numero_identificacion']
            if documento['empresa__digito_verificacion']:
                numero_identificacion = numero_identificacion+"-"+documento['empresa__digito_verificacion']
            direccion = ""
            if documento['empresa__direccion']:
                direccion = direccion+documento['empresa__direccion']
            if documento['empresa__ciudad__nombre']:
                direccion = direccion+" - "+documento['empresa__ciudad__nombre'].upper()
            p.setFont("Helvetica-Bold", 9)
            p.drawString(x + 75, 735, documento['empresa__nombre_corto'].upper() if documento['empresa__nombre_corto'] else "")
            p.setFont("Helvetica", 8)
            p.drawString(x + 75, 725, "NIT: " + numero_identificacion + (" - PERSONA " + documento['empresa__tipo_persona__nombre'].upper() if documento['empresa__tipo_persona__nombre'] else ""))
            p.drawString(x + 75, 715, "DIRECCIÓN: " + direccion)
            p.drawString(x + 75, 705, "TEL: " + documento['empresa__telefono'] if documento['empresa__telefono'] else "")


            #Datos factura
            p.setFont("Helvetica-Bold", 9)
            p.drawRightString(x + 540, 720, documento['documento_tipo__nombre'])
            p.setFont("Helvetica", 9)
            if documento['resolucion_id']:
                if documento['numero']:
                    texto_resolucion = documento['resolucion__prefijo'] + str(documento['numero'])
                else:
                    texto_resolucion = documento['resolucion__prefijo']
            else:
                texto_resolucion = ""
            p.setFont("Helvetica-Bold", 9)
            p.drawCentredString(x + 460, 710, texto_resolucion if texto_resolucion else  "")
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 350, 650, "FECHA EMISIÓN: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 560, 650, str(documento['fecha']))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 350, 640, "FECHA VENCIMIENTO: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 560, 640, str(documento['fecha_vence']))

            if documento['documento_tipo__documento_clase_id'] == 101 or documento['documento_tipo__documento_clase_id'] == 102:
                p.setFont("Helvetica-Bold", 8)
                p.drawString(x + 350, 630, "DOCUMENTO REFERENCIA: ")
                p.setFont("Helvetica", 8)
                p.drawRightString(x + 560, 630, str(documento['documento_referencia__numero']))
            else:
                if 'metodo_pago__nombre' in documento and documento['metodo_pago__nombre']:

                    p.setFont("Helvetica-Bold", 8)
                    p.drawString(x + 350, 630, "METODO DE PAGO: ")
                    p.setFont("Helvetica", 8)
                    p.drawRightString(x + 560, 630, str(documento['metodo_pago__nombre'].upper()))

                p.setFont("Helvetica-Bold", 8)
                p.drawString(x + 350, 620, "PLAZO PAGO: ")
                p.setFont("Helvetica", 8)
                p.drawRightString(x + 560, 620, str(documento['plazo_pago__nombre'] if documento['plazo_pago__nombre'] else ""))

                p.setFont("Helvetica-Bold", 8)
                p.drawString(x + 350, 610, "ORDEN COMPRA: ")
                p.setFont("Helvetica", 8)
                p.drawRightString(x + 560, 610, documento['orden_compra'] if documento['orden_compra'] else "")


            #Cliente
            clienteNombre = ""
            clienteCiudad = ""
            clienteCorreo = ""
            clienteTelefono = ""
            clienteIdentificacion = ""
            clienteDireccion = ""
            if documento['contacto_id'] is not None:
                 clienteNombre = documento['contacto__nombre_corto']
                 clienteCiudad = documento['contacto__ciudad__nombre']
                 clienteCorreo = documento['contacto__correo']
                 clienteTelefono = documento['contacto__telefono']
                 clienteIdentificacion =  documento['contacto__numero_identificacion']
                 clienteDireccion = documento['contacto__direccion']

            
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 650, "CLIENTE: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 60, 650, str(clienteNombre))
            
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 640, "NIT: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 60, 640, str(clienteIdentificacion))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 630, "DIRECCIÓN: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 60, 630, str(clienteDireccion))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 620, "CIUDAD: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 60, 620, str(clienteCiudad))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 610, "TELÉFONO: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 60, 610, str(clienteTelefono))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 600, "CORREO: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 60, 600, str(clienteCorreo))

            #Encabezado detalles
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 5, 575, "#")
            p.drawString(x + 30, 575, "COD")
            p.drawString(200, 575, "ÍTEM")
            p.drawString(x + 340, 575, "CANT")
            p.drawString(x + 380, 575, "PRECIO")
            p.drawString(x + 430, 575, "DESC")
            p.drawString(x + 470, 575, "IMPUESTO")
            p.drawString(x + 520, 575, "TOTAL")
            p.setFont("Helvetica", 8)

            x = 30

            valorLetras = convertir_a_letras(int(documento['total']))

            consecutivoDesde = ""
            consecutivoHasta = ""
            numero = ""
            fechaVigencia = ""
            if documento['resolucion_id']:
                consecutivoDesde = documento['resolucion__consecutivo_desde']
                consecutivoHasta = documento['resolucion__consecutivo_hasta']
                numero = documento['resolucion__numero']
                fechaVigencia = documento['resolucion__fecha_hasta']

            cue = ""
            if documento['cue']:
                cue = documento['cue']

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 120, str(valorLetras))

            p.drawString(x, 110, "CUFE/CUDE: ")
            p.setFont("Helvetica", 8)
            p.drawString(105, 110, str(cue))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 100, "NUMERO DE AUTORIZACIÓN:")
            p.setFont("Helvetica", 8)
            p.drawString(170, 100, str(numero))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(250, 100, "RANGO AUTORIZADO DESDE: ")
            p.setFont("Helvetica", 8)
            p.drawString(370, 100, str(consecutivoDesde))
            p.setFont("Helvetica-Bold", 8)
            p.drawString(400, 100, "HASTA: ")
            p.setFont("Helvetica", 8)
            p.drawString(432, 100, str(consecutivoHasta))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(465, 100, "VIGENCIA: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(550, 100, str(fechaVigencia) if fechaVigencia is not None else "")

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 90, "GENERADO POR: ")
            p.setFont("Helvetica", 8)
            p.drawString(110, 90, "REDDOC")

            p.setFont("Helvetica-Bold", 8)
            p.drawString(250, 90, "PROVEEDOR TECNOLÓGICO: ")
            p.setFont("Helvetica", 8)
            p.drawString(370, 90, "SOFTGIC S.A.S")

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 80, "FECHA VALIDACIÓN: ")
            p.setFont("Helvetica", 8)
            fecha = documento['fecha_validacion']
            if fecha:
                fecha_local = localtime(fecha)
                fecha_str = fecha_local.strftime('%Y-%m-%d %H:%M:%S')
            else:
                fecha_str = ""
            p.drawString(120, 80, fecha_str)            

            p.setStrokeColorRGB(0.8, 0.8, 0.8)
            p.setLineWidth(0.5)
            p.line(50, 45, 250, 45)
            p.setStrokeColorRGB(0, 0, 0)
            p.setFont("Helvetica-Bold", 8)
            p.drawCentredString(150, 30, "ELABORADO POR")

            p.setStrokeColorRGB(0.8, 0.8, 0.8)  # Color tenue (gris claro)
            p.setLineWidth(0.5)  # Grosor de la línea
            p.line(270, 45, 550, 45)  # Coordenadas para dibujar la segunda línea
            p.setStrokeColorRGB(0, 0, 0)  # Restaurar el color a negro
            p.drawCentredString(410, 30, "ACEPTADA, FIRMADA Y/O SELLO Y FECHA")
    
            p.drawCentredString(550, 20, "Página %d de %d" % (p.getPageNumber(), p.getPageNumber()))

            #informacion pago
            ancho_texto, alto_texto = informacionPago.wrapOn(p, 300, 400)
            
            #comentarios
            ancho_texto, alto_texto = comentario.wrapOn(p, 300, 400)
            
            x = 30
            y = 235 - alto_texto
            y2 = 160
            comentario.drawOn(p, x, y)
            informacionPago.drawOn(p, x, y2)


        def draw_totals(p, y, documento, documento_impuestos):

            x = 440
            totalFactura = documento['total']
            #Bloque totales
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 230, "SUBTOTAL")
            p.drawRightString(x + 140, 230,  f"{documento['subtotal']:,.0f}")
            
            # Crear un diccionario para almacenar los totales por impuesto_id y su nombre
            impuesto_totals = {}

            # Recorrer los objetos DocumentoImpuesto
            for impuesto in documento_impuestos:
                impuesto_id = impuesto['impuesto_id']  # ID del impuesto
                nombre_impuesto = impuesto['impuesto__nombre_extendido']  # Nombre del impuesto
                total = impuesto['total_operado']                
                if impuesto_id in impuesto_totals:
                    impuesto_totals[impuesto_id]['total'] += total
                else:
                    impuesto_totals[impuesto_id] = {'total': total, 'nombre': nombre_impuesto}

            # Definir la posición "y" inicial
            y = 220

            # Recorrer el diccionario de totales de impuestos
            for impuesto_id, data in impuesto_totals.items():
                nombre_impuesto = data['nombre']
                total_acumulado = data['total']
                
                p.drawString(x, y, nombre_impuesto.upper())
                p.drawRightString(x + 140, y, f"{total_acumulado:,.0f}")
                y -= 10

            p.drawString(x, y, "TOTAL GENERAL")
            p.drawRightString(x + 140, y, f"{totalFactura:,.0f}")
            
        y = 555

        # Inicialización
        draw_header()
        x = 24
        max_altura_disponible = 330  # Altura máxima disponible en la página para los ítems
        altura_acumulada = 0  # Altura acumulada por los ítems en la página
        y = 550  # Posición vertical inicial
        detalles_en_pagina = 0
        cantidad_total_items = 0

        documento_detalles = GenDocumentoDetalle.objects.filter(documento_id=documento['id']).values('id', 'cantidad', 'precio', 'descuento', 'subtotal', 'total','item__nombre', 'item_id')
        for index, detalle in enumerate(documento_detalles):

            itemNombre = ""
            if detalle['item__nombre'] is not None:
                itemNombre = detalle['item__nombre']

            documento_impuestos = GenDocumentoImpuesto.objects.filter(documento_detalle_id=detalle['id']).values(
                'id', 'total', 'total_operado', 'impuesto_id',
                'impuesto__nombre',
                'impuesto__nombre_extendido',  
                'impuesto__porcentaje',          
                'documento_detalle_id'
            ).order_by('impuesto_id')
            '''impuestos_detalle = [impuesto for impuesto in documento_impuestos if impuesto['documento_detalle_id'] == detalle['id']]
            total_impuestos_detalle = sum(impuesto['total'] for impuesto in impuestos_detalle)
            '''
            #impuestos = [str(item['impuesto__porcentaje']) for item in documento_impuestos]
            #impuestos = ', '.join(impuestos)
            impuestos = [f"{item['impuesto__porcentaje']:.1f}%" for item in documento_impuestos]
            impuestos = ', '.join(impuestos)

            item_nombre_paragraph = Paragraph(itemNombre, ParagraphStyle(name='ItemNombreStyle', fontName='Helvetica', fontSize=7))
            ancho, alto = item_nombre_paragraph.wrap(280, 100)
            
            altura_requerida = alto + 10  # Altura requerida incluyendo un margen adicional
            
            # Verificar si hay suficiente espacio para el siguiente ítem
            if altura_acumulada + altura_requerida > max_altura_disponible:
                p.showPage()
                y = 550  # Restablecer altura disponible para nueva página
                draw_header()
                altura_acumulada = 0
                detalles_en_pagina = 0

            item_nombre_paragraph.drawOn(p, x + 58, y - alto + 5)
            y -= altura_requerida
            altura_acumulada += altura_requerida

            p.setFont("Helvetica", 7)
            p.drawCentredString(x + 7, y + alto + 8, str(index + 1))
            p.drawString(x + 25, y + alto + 8, str(detalle['item_id']))
            p.drawRightString(x + 365, y + alto + 8, str(detalle['cantidad']))
            p.drawRightString(x + 417, y + alto + 8, f"{detalle['precio']:,.0f}")
            p.drawRightString(x + 458, y + alto + 8, f"{detalle['descuento']:,.0f}")
            p.drawString(x + 470, y + alto + 8, impuestos)
            p.drawRightString(x + 555, y + alto + 8, f"{detalle['subtotal']:,.0f}")

            y -= 10  # Ajuste de posición vertical para el siguiente ítem
            altura_acumulada += 10
            detalles_en_pagina += 1
            cantidad_total_items += 1

            if index == len(documento_detalles) - 1:
                draw_totals(p, y, documento, documento_impuestos)

        p.drawString(x + 5, y, "CANTIDAD DE ÍTEMS: " + str(cantidad_total_items))

        p.save()
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
