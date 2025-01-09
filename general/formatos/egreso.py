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
        p.setFont("Helvetica", 8)

        # Obtener datos del documento
        documento = GenDocumento.objects.filter(pk=id).values(
            "numero", "total", "fecha", "contacto__nombre_corto", "contacto__numero_identificacion", 'cuenta_banco__nombre'
        ).first()

        # Crear encabezado estructurado (como tabla)
        y = 680
        # Encabezado de la tabla
        # Encabezado de la tabla
        encabezado_data = [
            ["NUMERO:", str(documento["numero"] or ""), "CONTACTO:", f"{documento['contacto__numero_identificacion'] or ''} - {documento['contacto__nombre_corto'][:58] or ''}", "TOTAL:", f"{documento['total']:.2f}" if documento["total"] else "0"],
            ["FECHA:", documento["fecha"].strftime("%Y-%m-%d") if documento["fecha"] else "", "CUENTA:", f"{documento['cuenta_banco__nombre'] or ''}", "", ""]
        ]

        # Anchos de las columnas
        colWidths = [70, 70, 70, 200, 50, 80]

        # Crear la tabla
        encabezado_table = Table(encabezado_data, colWidths=colWidths)

        # Estilos optimizados
        styles = TableStyle([
            # Bordes generales
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            # Fuente y tamaño general
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            # Fondo gris y texto blanco para los títulos (primera y tercera columna)
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('BACKGROUND', (2, 0), (2, -1), colors.grey),
            ('BACKGROUND', (4, 0), (4, -1), colors.grey),  # Columna de "TOTAL"
            ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
            ('TEXTCOLOR', (2, 0), (2, -1), colors.white),
            ('TEXTCOLOR', (4, 0), (4, -1), colors.white),
            # Fondo blanco y texto negro para los valores (segunda, cuarta y sexta columna)
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('BACKGROUND', (3, 0), (3, -1), colors.white),
            ('BACKGROUND', (5, 0), (5, -1), colors.white),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            ('TEXTCOLOR', (3, 0), (3, -1), colors.black),
            ('TEXTCOLOR', (5, 0), (5, -1), colors.black),
            # Alineación
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Por defecto todo alineado a la izquierda
            ('ALIGN', (5, 0), (5, -1), 'RIGHT'),  # El valor de TOTAL alineado a la derecha
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical
            # Espaciado interno
            ('PADDING', (0, 0), (-1, -1), 4),
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
            fontSize=8,
            leading=10,  # Espaciado entre líneas
            alignment=TA_LEFT,
        )

        # Crear el contenido de la tabla
        data_details = [
            ["NUMERO", "CONTACTO", "CUENTA", "NATURALEZA", "PAGO"]
        ]  # Encabezados de la tabla

        documento_detalles = GenDocumentoDetalle.objects.filter(documento_id=id).values(
            "numero",
            "contacto__numero_identificacion",
            "contacto__nombre_corto",
            "cuenta__nombre",
            "cuenta__codigo",
            "naturaleza",
            "pago",
        )

        for detalle in documento_detalles:
            data_details.append([
                detalle["numero"] or "",
                Paragraph(detalle["contacto__nombre_corto"] or "", cell_style),
                Paragraph(f"{detalle['cuenta__codigo'] or ''} - {detalle['cuenta__nombre'] or ''}", cell_style),
                detalle["naturaleza"] or "",
                f"{detalle['pago']:.2f}" if detalle["pago"] else "",
            ])

        # Anchos fijos para las columnas
        colWidths_details = [60, 150, 150, 100, 80]

        # Crear tabla con estilo
        table_details = Table(data_details, colWidths=colWidths_details)
        table_details.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), grey),  # Fondo gris para encabezados
            ('TEXTCOLOR', (0, 0), (-1, 0), white),  # Texto blanco para encabezados
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación central
            ('GRID', (0, 0), (-1, -1), 0.5, black),  # Bordes de la tabla
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente para encabezados
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Fuente para el contenido
            ('FONTSIZE', (0, 0), (-1, -1), 8),  # Tamaño de fuente
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
