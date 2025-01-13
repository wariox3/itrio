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


class FormatoCompra:
    def __init__(self):
        self.encabezado = FormatoEncabezado()

    def generar_pdf(self, id):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setTitle("factura_compra")

        # Encabezado del documento
        self.encabezado.generar_pdf(p, "FACTURA DE COMPRA")
        p.setFont("Helvetica", 8)

        # Obtener datos del documento
        documento = GenDocumento.objects.filter(pk=id).values(
            "numero", "total", "fecha", 'fecha_vence' ,"contacto__nombre_corto", "contacto__numero_identificacion", 'plazo_pago__nombre', 'subtotal', 'impuesto_operado'
        ).first()

        # Crear encabezado estructurado (como tabla)
        y = 680
        # Encabezado de la tabla
        # Encabezado de la tabla
        encabezado_data = [
            ["NUMERO:", str(documento["numero"] or ""), "CONTACTO:", f"{documento['contacto__numero_identificacion'] or ''} - {documento['contacto__nombre_corto'][:28] or ''}", "TOTAL:", f"{documento['total']:.2f}" if documento["total"] else "0"],
            ["FECHA:", documento["fecha"].strftime("%Y-%m-%d") if documento["fecha"] else "", "PLAZO PAGO:", f"{documento['plazo_pago__nombre'].upper() or ''}", "", ""],
            ["FECHA VENCE:", documento["fecha_vence"].strftime("%Y-%m-%d") if documento["fecha_vence"] else ""]
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
            ["ID", "ITEM / CUENTA", "CANTIDAD", "PRECIO", "DESC", "SUBTOTAL", "NETO"]
        ]  # Encabezados de la tabla

        documento_detalles = GenDocumentoDetalle.objects.filter(documento_id=id).values(
            "id",
            "item__nombre",
            "cantidad",
            "precio",
            "descuento",
            "subtotal",
            "total",
            "cuenta__nombre",
            "cuenta__codigo"
        )

        total_cantidad = 0

        for detalle in documento_detalles:
            # Verificar si "item__nombre" tiene un valor, si no, usar "cuenta__codigo - cuenta__nombre"
            nombre = detalle["item__nombre"] or f'{detalle["cuenta__codigo"]} - {detalle["cuenta__nombre"]}'
            
            data_details.append([
                detalle["id"],
                Paragraph(nombre, cell_style),  # Usar el valor calculado
                detalle["cantidad"],
                "{:.2f}".format(detalle["precio"]),
                "{:.2f}".format(detalle["descuento"]),
                "{:.2f}".format(detalle["subtotal"]),
                "{:.2f}".format(detalle["total"]),
            ])

            total_cantidad += detalle["cantidad"]

        # Anchos fijos para las columnas
        colWidths_details = [20, 200, 60, 50, 50, 80, 80]

        # Crear tabla con estilo
        table_details = Table(data_details, colWidths=colWidths_details)
        table_details.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), grey),  # Fondo gris para encabezados
            ('TEXTCOLOR', (0, 0), (-1, 0), white),  # Texto blanco para encabezados
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Alineación central para encabezados
            ('ALIGN', (3, 1), (3, -1), 'RIGHT'),  # Alineación a la derecha para cantidad
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),  # Alineación a la derecha para precio
            ('ALIGN', (5, 1), (5, -1), 'RIGHT'),  # Alineación a la derecha para descyebti
            ('ALIGN', (5, 1), (5, -1), 'RIGHT'),  # Alineación a la derecha para subtotal
            ('ALIGN', (6, 1), (6, -1), 'RIGHT'),  # Alineación a la derecha para total
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

        y -= table_details._height + 20

        # Datos para la tabla de totales
        data_totals = [
            ["TOTAL CANTIDAD:", str(total_cantidad)],
            ["SUBTOTAL:", f"{documento['subtotal']:.2f}" if documento["subtotal"] else "0"],
            ["TOTAL IMPUESTO:", f"{documento['impuesto_operado']:.2f}" if documento["impuesto_operado"] else "0"],
            ["TOTAL GENERAL:", f"{documento['total']:.2f}" if documento["total"] else "0"],
        ]

        # Anchos de las columnas
        colWidths_totals = [90, 80]

        # Crear tabla de totales
        table_totals = Table(data_totals, colWidths=colWidths_totals)

        # Aplicar estilo uniforme a la tabla
        table_totals.setStyle(TableStyle([
            # Bordes de la tabla
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Bordes de todas las celdas

            # Fondo gris para la primera columna (campos de la izquierda)
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),  # Fondo gris en la primera columna
            ('TEXTCOLOR', (0, 0), (0, -1), colors.white),  # Texto blanco en la primera columna

            # Alineación de las celdas
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Alineación izquierda para la primera columna
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),  # Alineación derecha para la segunda columna

            # Fuente y tamaño de fuente consistente
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Fuente 'Helvetica' para todo el contenido
            ('FONTSIZE', (0, 0), (-1, -1), 8),  # Tamaño de fuente 8 para todas las celdas

            # Negrita solo para la primera fila (encabezado)
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Encabezados en negrita

            # Espaciado interno y alineación vertical uniforme
            ('PADDING', (0, 0), (-1, -1), 4),  # Espaciado uniforme
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical a 'MIDDLE' para todas las celdas
        ]))

        
        # Posicionar y dibujar la tabla de totales
        table_totals.wrapOn(p, 30, y)
        table_totals.drawOn(p, 400, y - table_totals._height) 

        # Finalizar el PDF
        p.save()

        # Obtener los bytes del PDF
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

