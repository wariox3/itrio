from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from reportlab.graphics import renderPDF
from utilidades.utilidades import convertir_a_letras
from utilidades.utilidades import generar_qr
import locale
from decouple import config

class FormatoCuentaCobro():

    def generar_pdf(self, data, configuracion):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        estilo_helvetica = ParagraphStyle(name='HelveticaStyle', fontName='Helvetica', fontSize=8)
        informacionPago = Paragraph("<b>INFORMACIÓN DE PAGO: </b>", estilo_helvetica)
        comentario = Paragraph("<b>COMENTARIOS: </b>" +  str(data['comentario'] if data['comentario'] else  ""), estilo_helvetica)

        try:
            locale.setlocale(locale.LC_ALL, 'es_CO.utf8')
        except locale.Error:
            pass

        def draw_header():

            region = config('DO_REGION')
            bucket = config('DO_BUCKET')
            entorno = config('ENV')

            imagen_defecto_url = f'https://{bucket}.{region}.digitaloceanspaces.com/itrio/{entorno}/empresa/logo_defecto.jpg'

            # Intenta cargar la imagen desde la URL
            imagen_empresa = data['empresa__imagen']

            logo_url = f'https://{bucket}.{region}.digitaloceanspaces.com/{imagen_empresa}'
            try:
                logo = ImageReader(logo_url)
            except Exception as e:
                # Si se produce un error, establece la URL en la imagen de defecto
                logo_url = imagen_defecto_url
                logo = ImageReader(logo_url)

            tamano_cuadrado = 1 * inch
            x = 24
            y = 680

            #borde tabla detalles
            p.drawImage(logo, x, y, width=tamano_cuadrado, height=tamano_cuadrado, mask='auto')
            p.setStrokeColorRGB(0.8, 0.8, 0.8)
            #recuadro1
            p.rect(x, 570, 564, 15)
            #recuadro2
            p.rect(x, 420, 564, 150)


            #Emisor
            p.setFont("Helvetica-Bold", 9)
            p.drawString(x + 75, 720, data['empresa__nombre_corto'].upper() if data['empresa__nombre_corto'] else "")
            p.setFont("Helvetica", 8)
            p.drawString(x + 75, 710, "PERSONA " + data['empresa__tipo_persona__nombre'].upper() if data['empresa__tipo_persona__nombre'] else "")
            p.drawString(x + 75, 700, "NIT: " + data['empresa__numero_identificacion'] + "-" +  data['empresa__digito_verificacion'])
            p.drawString(x + 75, 690, "DIRECCIÓN: " + data['empresa__direccion'].upper() + " - " +data['empresa__ciudad__nombre'].upper())
            p.drawString(x + 75, 680, "TEL: " + data['empresa__telefono'] if data['empresa__telefono'] else "")

            #Datos factura
            p.setFont("Helvetica-Bold", 9)
            p.drawCentredString(x + 460, 710, str(data['numero'] if data['numero'] else ""))
            p.setFont("Helvetica-Bold", 9)
            p.drawCentredString(x + 460, 720, "CUENTA DE COBRO")
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 350, 650, "FECHA EMISIÓN: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 540, 650, str(data['fecha']))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 350, 640, "FECHA VENCIMIENTO: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 540, 640, str(data['fecha_vence']))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 350, 630, "PLAZO PAGO: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 540, 630, "")

            if 'metodo_pago__nombre' in data and data['metodo_pago__nombre']:

                p.setFont("Helvetica-Bold", 8)
                p.drawString(x + 350, 620, "FORMA PAGO: ")
                p.setFont("Helvetica", 8)
                p.drawRightString(x + 540, 620, str(data['metodo_pago__nombre'].upper()))

            #Cliente
            clienteNombre = ""
            clienteCiudad = ""
            clienteCorreo = ""
            clienteTelefono = ""
            clienteIdentificacion = ""
            clienteDireccion = ""
            if data['contacto_id'] is not None:
                 clienteNombre = data['contacto__nombre_corto']
                 clienteCiudad = data['contacto__ciudad__nombre']
                 clienteCorreo = data['contacto__correo']
                 clienteTelefono = data['contacto__telefono']
                 clienteIdentificacion =  data['contacto__numero_identificacion']
                 clienteDireccion = data['contacto__direccion']


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
            p.drawString(x + 475, 575, "IVA")
            p.drawString(x + 520, 575, "TOTAL")
            p.setFont("Helvetica", 8)

        def draw_totals(p, y, data):

            x = 440
            totalFactura = data['total']

            #Bloque totales
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 410, "SUBTOTAL")
            p.drawRightString(x + 140, 410, f"$ {locale.format('%d', data['subtotal'], grouping=True)}")

            # Crear un diccionario para almacenar los totales por impuesto_id y su nombre
            impuesto_totals = {}

            # Recorrer los objetos DocumentoImpuesto
            for impuesto in data['documento_impuestos']:
                impuesto_id = impuesto['impuesto_id']  # ID del impuesto
                nombre_impuesto = impuesto['impuesto__nombre_extendido']  # Nombre del impuesto
                total = impuesto['total']

                # Verificar si el impuesto_id ya existe en el diccionario
                if impuesto_id in impuesto_totals:
                    # Si existe, sumar el total al valor existente
                    impuesto_totals[impuesto_id]['total'] += total
                else:
                    # Si no existe, crear una nueva entrada en el diccionario con el total y el nombre del impuesto
                    impuesto_totals[impuesto_id] = {'total': total, 'nombre': nombre_impuesto}

            # Definir la posición "y" inicial
            y = 395

            # Recorrer el diccionario de totales de impuestos
            for impuesto_id, data in impuesto_totals.items():
                nombre_impuesto = data['nombre']
                total_acumulado = data['total']

                p.drawString(x, y, nombre_impuesto.upper())
                p.drawRightString(x + 140, y, f"$ {locale.format('%d', total_acumulado, grouping=True)}")
                y -= 15

            p.drawString(x, y, "TOTAL GENERAL")
            p.drawRightString(x + 140, y, f"$ {locale.format('%d', totalFactura, grouping=True)}")

            #informacion pago
            # ancho_texto, alto_texto = informacionPago.wrapOn(p, 280, 380)

            #comentarios
            ancho_texto, alto_texto = comentario.wrapOn(p, 300, 400)

            x = 30
            y = 390 - alto_texto
            y2 = 160
            comentario.drawOn(p, x, y)
            # informacionPago.drawOn(p, x, y2)

        y = 555
        page_number = 1
        detalles_en_pagina = 0

        draw_header()
        x = 24

        for index, detalle in enumerate(data['documento_detalles']):

            itemNombre = ""
            if detalle['item__nombre'] is not None:
                itemNombre = detalle['item__nombre'][:100]

            impuestos_detalle = [impuesto for impuesto in data['documento_impuestos'] if impuesto['documento_detalle_id'] == detalle['id']]

            total_impuestos_detalle = sum(impuesto['total'] for impuesto in impuestos_detalle)

            p.setFont("Helvetica", 7)
            p.drawCentredString(x + 7, y, str(index + 1))
            p.drawString(x + 25, y, str(detalle['item_id']))
            p.drawString(x + 58, y, str(itemNombre[:70]))
            p.drawRightString(x + 365, y, str(int(detalle['cantidad'])))
            p.drawRightString(x + 417, y, locale.format_string("%d", detalle['precio'], grouping=True))
            p.drawRightString(x + 458, y, locale.format_string("%d", detalle['descuento'], grouping=True))
            p.drawRightString(x + 500, y, locale.format_string("%d", total_impuestos_detalle, grouping=True))
            p.drawRightString(x + 555, y, locale.format_string("%d", detalle['total'], grouping=True))
            y -= 30
            detalles_en_pagina += 1

            if detalles_en_pagina == 4 or index == len(data['documento_detalles']) - 1:
                draw_totals(p, y, data)

                if index != len(data['documento_detalles']) - 1:
                    p.showPage()
                    page_number += 1
                    y = 520
                    draw_header()
                    detalles_en_pagina = 0

        p.drawString(x + 5, y, "CANTIDAD DE ÍTEMS: " + str(detalles_en_pagina))
        def draw_footer(pageCount):
            x = 30

            valorLetras = convertir_a_letras(int(data['total']))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 410, "VALOR EN LETRAS: " + str(valorLetras))

            p.drawCentredString(550, 20, "Página %d de %d" % (p.getPageNumber(), pageCount))

        total_pages = p.getPageNumber()

        draw_footer(total_pages)

        p.save()

        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes