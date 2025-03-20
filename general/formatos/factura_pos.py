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
from datetime import datetime 
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

class FormatoFacturaPOS():

    def generar_pdf(self, id):
        # Tamaño personalizado para POS (80 mm de ancho x 200 mm de alto)
        POS_SIZE = (80 * mm, 200 * mm)
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=POS_SIZE)
        p.setTitle("Factura POS")
        documento = GenDocumento.objects.select_related('empresa', 'documento_tipo', 'contacto', 'resolucion', 'metodo_pago', 'contacto__ciudad', 'empresa__tipo_persona', 'documento_referencia', 'plazo_pago').filter(id=id).values(
        'id', 'fecha', 'fecha_validacion', 'fecha_vence', 'numero', 'soporte', 'qr', 'cue', 'resolucion_id', 'contacto_id',
        'subtotal', 'total', 'comentario', 'orden_compra', 'metodo_pago__nombre',
        'contacto__nombre_corto', 'contacto__correo', 'contacto__telefono', 'contacto__numero_identificacion', 'contacto__direccion', 
        'contacto__ciudad__nombre', 
        'empresa__tipo_persona__nombre', 'empresa__numero_identificacion', 'empresa__digito_verificacion', 'empresa__direccion', 'empresa__telefono',
        'empresa__nombre_corto', 'empresa__imagen', 'empresa__ciudad__nombre', 'documento_tipo__nombre', 'resolucion__prefijo',
        'resolucion__consecutivo_desde', 'resolucion__consecutivo_hasta', 'resolucion__numero', 'resolucion__fecha_hasta', 'resolucion__fecha_desde',
        'documento_referencia__numero', 'documento_tipo__documento_clase_id', 'plazo_pago__nombre'
        ).first()

        estilo_item = ParagraphStyle(
        name='ItemStyle',
        fontName='Courier',
        fontSize=7,
        leading=7,  # Espacio entre líneas
        spaceAfter=4,  # Espacio después del párrafo
        leftIndent=0,  # Sangría izquierda
        rightIndent=0,  # Sangría derecha
        wordWrap=True,  # Ajuste de texto
        )

        # Estilo para la cantidad y el subtotal (alineados a la derecha)
        estilo_derecha = ParagraphStyle(
            name='DerechaStyle',
            fontName='Courier',
            fontSize=7,
            leading=6,
            alignment=2,  # 0=Izquierda, 1=Centro, 2=Derecha
        )

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

        # Margen izquierdo y posición inicial
        x = 5 * mm
        y = POS_SIZE[1] - 10 * mm  # Comienza cerca del borde superior

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

        # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.now()

        # Formatear la fecha y hora como desees (por ejemplo, "dd/mm/yyyy HH:M
        fecha_hora_texto = fecha_hora_actual.strftime('%Y/%m/%d %H:%M:%S')

        y -= 5 * mm 

        # Dibujar datos alineados a la izquierda
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
        p.drawString(x, y, "ÍTEM")  # Columna para el nombre del ítem
        p.drawString(x + 40 * mm, y, "CANT")  # Columna para la cantidad
        p.drawString(x + 55 * mm, y, "SUBTOTAL")  # Columna para el subtotal
        y -= 8 * mm  # Espacio entre el encabezado y los detalles

        # Configurar la fuente para los detalles de los ítems
        p.setFont("Courier", 7)
        cantidad_total_items = 0
        for detalle in documento_detalles:
            # Dibujar el nombre del ítem (usando Paragraph para ajuste de texto)
            item_paragraph = Paragraph(detalle['item__nombre'], estilo_item)
            item_paragraph.wrapOn(p, 40 * mm, 20 * mm)  # Ancho máximo de 50 mm, altura máxima de 20 mm
            item_paragraph.drawOn(p, x, y - item_paragraph.height + 4 * mm)  # Ajustar posición y
            
            # Dibujar la cantidad (alineada a la derecha)
            cantidad_paragraph = Paragraph(str(detalle['cantidad']), estilo_derecha)
            cantidad_paragraph.wrapOn(p, 10 * mm, 20 * mm)  # Ancho máximo de 10 mm
            cantidad_paragraph.drawOn(p, x + 40 * mm, y - cantidad_paragraph.height + 4 * mm)
            
            # Dibujar el subtotal (alineado a la derecha)
            subtotal_paragraph = Paragraph(f"{detalle['subtotal']:,.0f}", estilo_derecha)
            subtotal_paragraph.wrapOn(p, 20 * mm, 20 * mm)  # Ancho máximo de 20 mm
            subtotal_paragraph.drawOn(p, x + 50 * mm, y - subtotal_paragraph.height + 4 * mm)
            
            # Ajustar la coordenada y para la siguiente fila
            y -= max(item_paragraph.height, cantidad_paragraph.height, subtotal_paragraph.height) + 1 * mm
            cantidad_total_items += 1
        # Línea divisoria
        dibujar_linea(p, x, y, POS_SIZE[0] - x, y, punteada=True, grosor=0.5)
        y -= 5 * mm

        # Totales
        p.setFont("Courier-Bold", 7)
        p.drawString(x, y, "TOTAL:")
        p.drawRightString(x + 70 * mm, y, f"{documento['total']:,.0f}")
        y -= 4 * mm

        p.setFont("Courier-Bold", 7)
        p.drawString(x, y, "TOTAL ITEMS:")
        p.drawRightString(x + 70 * mm, y, str(cantidad_total_items))
        y -= 4 * mm

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
            cue_paragraph.wrapOn(p, 60 * mm, 20 * mm)  # Ajustar ancho y alto máximo
            cue_paragraph.drawOn(p, x, y - cue_paragraph.height + 4 * mm)
            y -= cue_paragraph.height + 8 * mm  # Ajustar y basado en la altura real del párrafo

        # QR (si es necesario)
        if documento['qr']:
            qr_code_drawing = generar_qr(documento['qr'])  # Asegúrate de tener esta función
            qr_size = 20 * mm  # Tamaño del QR
            qr_x = (POS_SIZE[0] - qr_size - 30) / 2  # Centrar horizontalmente
            qr_y = y - qr_size  # Posicionar verticalmente
            renderPDF.draw(qr_code_drawing, p, qr_x, qr_y)
            y -= qr_size + 6 * mm  # Ajustar y para lo siguiente en el documento

        # Pie de página
        # p.setFont("Helvetica", 6)
        # p.drawCentredString(POS_SIZE[0] / 2, y, "Gracias por su compra")
        # y -= 5 * mm
        # p.drawCentredString(POS_SIZE[0] / 2, y, "Sistema de Facturación POS")

        # Finalizar el PDF
        p.showPage()
        p.save()

        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

def dibujar_campo_centrado(canvas, texto, x, y, font_name="Courier", font_size=8, leading=4):
    """
    Dibuja un texto centrado en la coordenada x y ajusta la coordenada y.
    """
    canvas.setFont(font_name, font_size)
    canvas.drawCentredString(x, y, texto)
    y -= leading * mm 
    return y

def dibujar_campo_izquierda(canvas, texto, x, y, font_name="Courier", font_size=8, leading=4):
    """
    Dibuja un texto alineado a la izquierda en la coordenada x y ajusta la coordenada y.
    """
    canvas.setFont(font_name, font_size)
    canvas.drawString(x, y, texto) 
    y -= leading * mm  
    return y


def dibujar_linea(canvas, x1, y1, x2, y2, punteada=False, grosor=1):
    """
    Dibuja una línea en el canvas.

    Parámetros:
    - canvas: Objeto canvas de ReportLab.
    - x1, y1: Coordenadas de inicio de la línea.
    - x2, y2: Coordenadas de fin de la línea.
    - punteada: Si es True, la línea será punteada. Si es False, será sólida.
    - grosor: Grosor de la línea (por defecto 1).
    """
    # Configurar el grosor de la línea
    canvas.setLineWidth(grosor)

    # Configurar el patrón de línea (sólida o punteada)
    if punteada:
        canvas.setDash([2, 2])  # Línea punteada (guiones de 2 puntos, espacios de 2 puntos)
    else:
        canvas.setDash([])  # Línea sólida

    # Dibujar la línea
    canvas.line(x1, y1, x2, y2)

    # Restaurar el patrón de línea sólida (opcional, para no afectar otras líneas)
    canvas.setDash([])