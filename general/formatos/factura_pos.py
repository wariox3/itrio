from reportlab.lib.pagesizes import mm
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas
from io import BytesIO
from utilidades.utilidades import generar_qr
from reportlab.graphics import renderPDF
from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from general.models.documento_impuesto import GenDocumentoImpuesto
from datetime import datetime 
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from django.db.models import Sum
from collections import defaultdict

class FormatoFacturaPOS():

    def generar_pdf(self, id):
        # Tamaño inicial para POS (80 mm de ancho x altura dinámica)
        ANCHO_POS = 80 * mm
        ALTURA_INICIAL = 200 * mm  # Altura inicial, se ajustará dinámicamente

        buffer = BytesIO()
        documento = GenDocumento.objects.select_related('empresa', 'documento_tipo', 'contacto', 'resolucion', 'metodo_pago', 'contacto__ciudad', 'empresa__tipo_persona', 'documento_referencia', 'plazo_pago').filter(id=id).values(
        'id', 'fecha', 'fecha_validacion', 'fecha_vence', 'numero', 'soporte', 'qr', 'cue', 'resolucion_id', 'contacto_id',
        'subtotal', 'total', 'comentario', 'orden_compra', 'metodo_pago__nombre',
        'contacto__nombre_corto', 'contacto__correo', 'contacto__telefono', 'contacto__numero_identificacion', 'contacto__direccion', 
        'contacto__ciudad__nombre', 
        'empresa__tipo_persona__nombre', 'empresa__numero_identificacion', 'empresa__digito_verificacion', 'empresa__direccion', 'empresa__telefono',
        'empresa__nombre_corto', 'empresa__imagen', 'empresa__ciudad__nombre', 'documento_tipo__nombre', 'resolucion__prefijo',
        'resolucion__consecutivo_desde', 'resolucion__consecutivo_hasta', 'resolucion__numero', 'resolucion__fecha_hasta', 'resolucion__fecha_desde',
        'documento_referencia__numero', 'documento_tipo__documento_clase_id', 'plazo_pago__nombre', 'impuesto', 'base_impuesto'
        ).first()

        estilo_item = ParagraphStyle(
            name='ItemStyle',
            fontName='Courier',
            fontSize=7,
            leading=7,
            spaceAfter=4,
            leftIndent=0,
            rightIndent=0,
            wordWrap=True,
        )

        estilo_derecha = ParagraphStyle(
            name='DerechaStyle',
            fontName='Courier',
            fontSize=7,
            leading=6,
            alignment=2,
        )

        # Calcular la altura total requerida
        altura_total = self.calcular_altura_total(documento, estilo_item, estilo_derecha)

        # Ajustar el tamaño de la página
        POS_SIZE = (ANCHO_POS, altura_total)

        p = canvas.Canvas(buffer, pagesize=POS_SIZE)
        p.setTitle("Factura POS")

        # Emisor
        numero_identificacion = ""
        if documento['empresa__numero_identificacion']:
            numero_identificacion = numero_identificacion + documento['empresa__numero_identificacion']
        if documento['empresa__digito_verificacion']:
            numero_identificacion = numero_identificacion + "-" + documento['empresa__digito_verificacion']
        direccion = ""
        if documento['empresa__direccion']:
            direccion = direccion + documento['empresa__direccion']
        if documento['empresa__ciudad__nombre']:
            direccion = direccion + " - " + documento['empresa__ciudad__nombre'].upper()

        # Margen izquierdo y posición inicial
        x = 5 * mm
        y = POS_SIZE[1] - 10 * mm

        # Encabezado
        p.setFont("Courier", 8)
        nombre_empresa = documento['empresa__nombre_corto'].upper() if documento['empresa__nombre_corto'] else ""
        y = dibujar_campo_centrado(p, nombre_empresa, POS_SIZE[0] / 2, y, font_name="Courier-Bold", font_size=8)

        nit_texto = f"NIT: {numero_identificacion}"
        y = dibujar_campo_centrado(p, nit_texto, POS_SIZE[0] / 2, y, font_size=7)

        direccion_texto = direccion
        y = dibujar_campo_centrado(p, direccion_texto, POS_SIZE[0] / 2, y, font_size=7)

        telefono_texto = f"Teléfono: {documento['empresa__telefono']}"
        y = dibujar_campo_centrado(p, telefono_texto, POS_SIZE[0] / 2, y, font_size=7)

        fecha_hora_texto = documento['fecha'].strftime('%Y/%m/%d')

        y -= 5 * mm

        # Dibujar datos alineados a la izquierda
        y = dibujar_campo_izquierda(p, f"Número:  {documento['numero'] or ''}", x, y, font_size=7)
        y = dibujar_campo_izquierda(p, f"Fecha:  {fecha_hora_texto}", x, y, font_size=7)
        y = dibujar_campo_izquierda(p, f"Cliente:  {documento['contacto__nombre_corto']}", x, y, font_size=7)
        y = dibujar_campo_izquierda(p, f"Nit/C.C:  {documento['contacto__numero_identificacion']}", x, y, font_size=7)
        y = dibujar_campo_izquierda(p, f"Dirección: {documento['contacto__direccion']}", x, y, font_size=7)
        y = dibujar_campo_izquierda(p, f"Teléfono: {documento['contacto__telefono']}", x, y, font_size=7)

        # Línea divisoria
        dibujar_linea(p, x, y, POS_SIZE[0] - x, y, punteada=True, grosor=0.5)
        y -= 5 * mm

        documento_detalles = GenDocumentoDetalle.objects.filter(documento_id=documento['id']).values('id', 'cantidad', 'precio', 'descuento', 'subtotal', 'impuesto', 'total','item__nombre', 'item_id')

        p.setFont("Courier-Bold", 7)
        p.drawString(x, y, "Ítem")
        p.drawString(x + 40 * mm, y, "Cant")
        p.drawString(x + 55 * mm, y, "Subtotal")
        y -= 8 * mm

        p.setFont("Courier", 7)
        cantidad_total_items = 0
        for detalle in documento_detalles:
            item_paragraph = Paragraph(detalle['item__nombre'], estilo_item)
            item_paragraph.wrapOn(p, 40 * mm, 20 * mm)
            item_paragraph.drawOn(p, x, y - item_paragraph.height + 4 * mm)

            cantidad_paragraph = Paragraph(str(detalle['cantidad']), estilo_derecha)
            cantidad_paragraph.wrapOn(p, 10 * mm, 20 * mm)
            cantidad_paragraph.drawOn(p, x + 40 * mm, y - cantidad_paragraph.height + 4 * mm)

            subtotal_paragraph = Paragraph(f"{detalle['subtotal']:,.0f}", estilo_derecha)
            subtotal_paragraph.wrapOn(p, 20 * mm, 20 * mm)
            subtotal_paragraph.drawOn(p, x + 50 * mm, y - subtotal_paragraph.height + 4 * mm)

            y -= max(item_paragraph.height, cantidad_paragraph.height, subtotal_paragraph.height) + 1 * mm
            cantidad_total_items += 1

        dibujar_linea(p, x, y, POS_SIZE[0] - x, y, punteada=True, grosor=0.5)
        y -= 5 * mm

        p.setFont("Courier-Bold", 7)
        p.drawString(x, y, "Total:")
        p.drawRightString(x + 70 * mm, y, f"{documento['total']:,.0f}")
        y -= 4 * mm

        p.drawString(x, y, "Total items:")
        p.drawRightString(x + 70 * mm, y, str(cantidad_total_items))
        y -= 4 * mm

        dibujar_linea(p, x, y, POS_SIZE[0] - x, y, punteada=True, grosor=0.5)
        y -= 4 * mm

        p.drawString(x, y, "Vta gravada:")
        p.drawRightString(x + 70 * mm, y, f"{documento['subtotal']:,.0f}")
        y -= 4 * mm

        p.drawString(x, y, "Impuestos:")
        p.drawRightString(x + 70 * mm, y, f"{documento['impuesto']:,.0f}")
        y -= 4 * mm

        dibujar_linea(p, x, y, POS_SIZE[0] - x, y, punteada=True, grosor=0.5)
        y -= 4 * mm

        p.drawString(x, y, "Descripción")
        p.drawString(x + 36 * mm, y, "Vr base")
        p.drawString(x + 55 * mm, y, "Vr impto")
        y -= 4 * mm

        documento_impuestos = GenDocumentoImpuesto.objects.filter(
            documento_detalle__documento_id=documento['id']
        ).values(
            'impuesto_id', 'impuesto__nombre_extendido', 'base', 'total_operado'
        ).order_by('impuesto_id')

        # Diccionario para acumular los valores por tipo de impuesto
        acumulador_impuestos = defaultdict(lambda: {'base': 0, 'total_operado': 0})

        # Acumular los valores
        for impuesto in documento_impuestos:
            nombre_impuesto = impuesto['impuesto__nombre_extendido']
            base = impuesto['base']
            total_operado = impuesto['total_operado']
            
            # Sumar al acumulador
            acumulador_impuestos[nombre_impuesto]['base'] += base
            acumulador_impuestos[nombre_impuesto]['total_operado'] += total_operado

        # Configuración de impresión
        espaciado_linea = 4 * mm
        p.setFont("Courier", 7)

        # Imprimir los resultados acumulados
        for nombre_impuesto, valores in acumulador_impuestos.items():
            total_base = valores['base']
            total_acumulado = valores['total_operado']
            
            p.drawString(x, y, nombre_impuesto)
            p.drawRightString(x + 50 * mm, y, f"{total_base :,.0f}")
            p.drawRightString(x + 70 * mm, y, f"{total_acumulado :,.0f}")
            y -= espaciado_linea

        dibujar_linea(p, x, y, POS_SIZE[0] - x, y, punteada=True, grosor=0.5)
        y -= 8 * mm

        resolucion_numero = documento.get('resolucion__numero')
        resolucion_prefijo = documento.get('resolucion__prefijo')
        resolucion_desde = documento.get('resolucion__consecutivo_desde')
        resolucion_hasta = documento.get('resolucion__consecutivo_hasta')
        resolucion_fecha_desde = documento.get('resolucion__fecha_desde')

        if resolucion_numero:
            y = dibujar_campo_izquierda(p, f"Resolución: {resolucion_numero} {resolucion_fecha_desde}", x, y, font_size=7)
            y = dibujar_campo_izquierda(p, f"Prefijo: {resolucion_prefijo} del No. {resolucion_desde} al {resolucion_hasta}", x, y, font_size=7)
            y -= 4 * mm

        if documento['cue']:
            cue_paragraph = Paragraph(f"Cufe: {documento['cue']}", estilo_item)
            cue_paragraph.wrapOn(p, 60 * mm, 20 * mm)
            cue_paragraph.drawOn(p, x, y - cue_paragraph.height + 4 * mm)
            y -= 8 * mm
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            y = dibujar_campo_izquierda(p, f"Fecha aceptación DIAN:", x, y, font_size=7)
            y = dibujar_campo_izquierda(p, f"{fecha_actual}", x, y, font_size=7)
            y -= cue_paragraph.height + 8 * mm

        if documento['qr']:
            qr_code_drawing = generar_qr(documento['qr'])
            qr_size = 20 * mm
            qr_x = (POS_SIZE[0] - qr_size - 30) / 2
            qr_y = y - qr_size
            renderPDF.draw(qr_code_drawing, p, qr_x, qr_y)
            y -= qr_size + 4 * mm
            y = dibujar_campo_centrado(p, "Proveedor tecnológico KIAI S.A.S", POS_SIZE[0] / 2, y, font_name="Courier-Bold", font_size=8)
            y = dibujar_campo_centrado(p, "Nit: 901337751 - 9", POS_SIZE[0] / 2, y, font_name="Courier-Bold", font_size=8)


        p.showPage()
        p.save()

        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    def calcular_altura_total(self, documento, estilo_item, estilo_derecha):
        """
        Calcula la altura total requerida para el contenido del PDF.
        """
        altura_total = 10 * mm  # Margen superior inicial

        # Encabezado
        altura_total += 4 * mm  # Nombre de la empresa
        altura_total += 4 * mm  # NIT
        altura_total += 4 * mm  # Dirección
        altura_total += 4 * mm  # Teléfono
        altura_total += 5 * mm  # Espacio adicional

        # Datos del cliente
        altura_total += 4 * mm  # Fecha
        altura_total += 4 * mm  # Cliente
        altura_total += 4 * mm  # Nit/C.C
        altura_total += 4 * mm  # Dirección
        altura_total += 4 * mm  # Teléfono
        altura_total += 5 * mm  # Línea divisoria

        # Detalles de los ítems
        altura_total += 8 * mm  # Encabezado de la tabla
        documento_detalles = GenDocumentoDetalle.objects.filter(documento_id=documento['id']).values('id', 'cantidad', 'precio', 'descuento', 'subtotal', 'impuesto', 'total','item__nombre', 'item_id')
        for detalle in documento_detalles:
            item_paragraph = Paragraph(detalle['item__nombre'], estilo_item)
            item_paragraph.wrapOn(None, 40 * mm, 20 * mm)
            altura_total += max(item_paragraph.height, 7 * mm) + 1 * mm

        altura_total += 5 * mm  # Línea divisoria

        # Totales
        altura_total += 4 * mm  # Total
        altura_total += 4 * mm  # Total items
        altura_total += 4 * mm  # Línea divisoria
        altura_total += 4 * mm  # Vta gravada
        altura_total += 4 * mm  # Impuestos
        altura_total += 4 * mm  # Línea divisoria

        # Impuestos
        documento_impuestos = GenDocumentoImpuesto.objects.filter(
            documento_detalle__documento_id=documento['id']
        ).values(
            'impuesto_id', 'impuesto__nombre_extendido', 'base'
        ).annotate(
            total_operado=Sum('total_operado')
        ).order_by('impuesto_id')

        altura_total += 4 * mm  # Encabezado de impuestos
        altura_total += len(documento_impuestos) * 4 * mm  # Cada impuesto

        altura_total += 8 * mm  # Línea divisoria

        # Resolución y CUFE
        if documento.get('resolucion__numero'):
            altura_total += 4 * mm  # Resolución
            altura_total += 4 * mm  # Prefijo

        if documento['cue']:
            cue_paragraph = Paragraph(f"Cufe: {documento['cue']}", estilo_item)
            cue_paragraph.wrapOn(None, 60 * mm, 20 * mm)
            altura_total += cue_paragraph.height + 8 * mm

        # QR
        if documento['qr']:
            altura_total += 26 * mm + 4 * mm  # Tamaño del QR + espacio adicional

        return altura_total

def dibujar_campo_centrado(canvas, texto, x, y, font_name="Courier", font_size=8, leading=4):
    canvas.setFont(font_name, font_size)
    canvas.drawCentredString(x, y, texto)
    y -= leading * mm 
    return y

def dibujar_campo_izquierda(canvas, texto, x, y, font_name="Courier", font_size=8, leading=4):
    canvas.setFont(font_name, font_size)
    canvas.drawString(x, y, texto) 
    y -= leading * mm  
    return y

def dibujar_linea(canvas, x1, y1, x2, y2, punteada=False, grosor=1):
    canvas.setLineWidth(grosor)
    if punteada:
        canvas.setDash([2, 2])
    else:
        canvas.setDash([])
    canvas.line(x1, y1, x2, y2)
    canvas.setDash([])