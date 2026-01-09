from reportlab.lib.colors import black, grey, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from general.formatos.encabezado import FormatoEncabezado
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors


class FormatoEgreso:
    def __init__(self):
        self.encabezado = FormatoEncabezado()

    def generar_pdf(self, id):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setTitle("recibo_de_caja")

        # Encabezado del documento
        self.encabezado.generar_pdf(p, "EGRESO")
        p.setFont("Helvetica", 6)

        # Obtener datos del documento
        documento = GenDocumento.objects.filter(pk=id).values(
            "numero", "total", "fecha", "contacto__nombre_corto", 
            "contacto__numero_identificacion", 'cuenta_banco__nombre', 'cuenta_banco__numero_cuenta' ,'contacto__direccion', 'contacto__telefono', 'contacto__ciudad__nombre'
        ).first()

        # Crear encabezado estructurado (como tabla)
        y = 680
        # Encabezado de la tabla
        encabezado_data = [
            # Fila 1: NUMERO - FECHA PAGO - CUENTA
            ["NUMERO:", str(documento["numero"] or ""), 
             "FECHA PAGO:", documento["fecha"].strftime("%Y-%m-%d") if documento["fecha"] else "", 
             "CUENTA:", documento.get("cuenta_banco__nombre", "") or ""],
            
            # Fila 2: CONTACTO - CIUDAD - NÚMERO CUENTA
            ["CONTACTO:", f"{documento['contacto__numero_identificacion'] or ''} - {documento['contacto__nombre_corto'][:40] or ''}", 
             "CIUDAD:", documento.get("contacto__ciudad__nombre", "") or "", 
             "NÚM CUENTA:", documento.get("cuenta_banco__numero_cuenta", "") or ""],

            
            # Fila 3: DIRECCIÓN - TELÉFONO - TOTAL
            ["DIRECCIÓN:", documento.get("contacto__direccion", "") or "", 
             "TELÉFONO:", documento.get("contacto__telefono", "") or "", 
             "TOTAL:", f"{documento['total']:,.0f}" if documento["total"] else "0"],
        ]

        # Anchos de las columnas (6 columnas: etiqueta + valor por cada campo)
        colWidths = [60, 190, 64, 70, 50, 105]

        # Crear la tabla
        encabezado_table = Table(encabezado_data, colWidths=colWidths)

        # Estilos optimizados
        styles = TableStyle([
            # Bordes generales
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            # Fuente y tamaño general
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 6),
            # Fondo gris y texto blanco para los títulos (todas las columnas impares: 0, 2, 4)
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('BACKGROUND', (2, 0), (2, -1), colors.grey),
            ('BACKGROUND', (4, 0), (4, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
            ('TEXTCOLOR', (2, 0), (2, -1), colors.white),
            ('TEXTCOLOR', (4, 0), (4, -1), colors.white),
            # Fondo blanco y texto negro para los valores (todas las columnas pares: 1, 3, 5)
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('BACKGROUND', (3, 0), (3, -1), colors.white),
            ('BACKGROUND', (5, 0), (5, -1), colors.white),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            ('TEXTCOLOR', (3, 0), (3, -1), colors.black),
            ('TEXTCOLOR', (5, 0), (5, -1), colors.black),
            # Alineación - TODO A LA IZQUIERDA excepto el valor de TOTAL
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),   # Por defecto todo a la izquierda
            
            # Valores de CUENTA (columna 5, fila 0) a la IZQUIERDA
            ('ALIGN', (5, 0), (5, 0), 'LEFT'),     # Valor de CUENTA a la izquierda
            
            # Valores de NÚMERO CUENTA (columna 5, fila 1) a la IZQUIERDA  
            ('ALIGN', (5, 1), (5, 1), 'LEFT'),     # Valor de NÚMERO CUENTA a la izquierda
            
            # Valor de TOTAL (columna 5, fila 2) a la DERECHA
            ('ALIGN', (5, 2), (5, 2), 'RIGHT'),    # Valor de TOTAL a la derecha
            
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical
            # Espaciado interno
            ('PADDING', (0, 0), (-1, -1), 4),
            # Altura de fila
            ('LEADING', (0, 0), (-1, -1), 12),
        ])

        # Aplicar los estilos
        encabezado_table.setStyle(styles)

        # Dibujar la tabla
        encabezado_table.wrapOn(p, 30, y)
        encabezado_table.drawOn(p, 30, y - encabezado_table._height)

        # Segunda tabla: Detalles del documento
        y -= 80  # Ajustar espacio entre encabezado y la tabla de detalles

        # Estilo para las celdas de texto
        cell_style = ParagraphStyle(
            name="CellStyle",
            fontName="Helvetica",
            fontSize=6,
            leading=10,  # Espaciado entre líneas
            alignment=TA_LEFT,
        )

        # Crear el contenido de la tabla - AÑADIR COLUMNA "REFERENCIA"
        data_details = [
            ["NUMERO", "REFERENCIA", "CONTACTO", "CUENTA", "NATURALEZA", "PAGO"]
        ]  # Encabezados de la tabla

        # Añadir el campo referencia_numero en la consulta
        documento_detalles = GenDocumentoDetalle.objects.filter(documento_id=id).values(
            "numero",
            "contacto__numero_identificacion",
            "contacto__nombre_corto",
            "cuenta__nombre",
            "cuenta__codigo",
            "naturaleza",
            "precio",
            "documento_afectado__referencia_numero",  # Agregar el campo de referencia
        )

        for detalle in documento_detalles:
            # Obtener la referencia si existe, de lo contrario vacío
            referencia = detalle.get("documento_afectado__referencia_numero", "")
            if referencia is None:
                referencia = ""
            
            data_details.append([
                detalle["numero"] or "",
                referencia,  # Agregar el campo de referencia
                Paragraph(detalle["contacto__nombre_corto"] or "", cell_style),
                Paragraph(f"{detalle['cuenta__codigo'] or ''} - {detalle['cuenta__nombre'] or ''}", cell_style),
                detalle["naturaleza"] or "",
                f"{detalle['precio']:,.0f}" if detalle["precio"] else "",
            ])

        # Ajustar los anchos de las columnas para incluir la nueva columna
        colWidths_details = [60, 80, 130, 130, 80, 60]  # Reducir otras columnas para hacer espacio

        # Crear tabla con estilo
        table_details = Table(data_details, colWidths=colWidths_details)
        table_details.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), grey),  # Fondo gris para encabezados
            ('TEXTCOLOR', (0, 0), (-1, 0), white),  # Texto blanco para encabezados
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación central por defecto
            # Alinear el campo PRECIO a la derecha (columna 5, desde fila 1 en adelante)
            ('ALIGN', (5, 1), (5, -1), 'RIGHT'),    # Solo la columna de PRECIO a la derecha
            ('GRID', (0, 0), (-1, -1), 0.5, black),  # Bordes de la tabla
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente para encabezados
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Fuente para el contenido
            ('FONTSIZE', (0, 0), (-1, -1), 6),  # Tamaño de fuente
            ('PADDING', (0, 0), (-1, -1), 4),  # Espaciado interno
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alineación vertical
        ]))

        # Dibujar tabla de detalles
        table_details.wrapOn(p, 30, y)
        table_details.drawOn(p, 30, y - table_details._height)

        # Finalizar el PDF
        p.save()

        # Obtener los bytes del PDF
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes