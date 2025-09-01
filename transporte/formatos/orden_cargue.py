from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle ,Spacer
from general.formatos.encabezado import FormatoEncabezado
from reportlab.lib.units import inch
from utilidades.pdf_utilidades import PDFUtilidades
from transporte.models.despacho import TteDespacho
from transporte.models.despacho_detalle import TteDespachoDetalle
from reportlab.lib import colors


class FormatoOrdenCargue:
    def generar_pdf(self, despacho_id):
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=0.4*inch, rightMargin=0.4*inch,
            topMargin=1.1*inch, bottomMargin=0.5*inch
        )
        
        elementos = []
        estilos = PDFUtilidades.obtener_estilos()
        def _encabezado(canvas, doc):
            FormatoEncabezado().generar_pdf(canvas, "ORDEN DE CARGUE")
        
        despacho = TteDespacho.objects.get(id=despacho_id)
        despacho_detalles = TteDespachoDetalle.objects.filter(despacho_id=despacho_id)
        fecha_formateada = despacho.fecha.strftime("%Y-%m-%d") if despacho.fecha else "N/A"

        elementos.append(Spacer(1,20))

        fila1_data = [
            Paragraph("Despacho:", estilos['etiqueta']),
            Paragraph(str(despacho.id), estilos['dato']),
            Paragraph("Vehículo:", estilos['etiqueta']),
            Paragraph(str(despacho.vehiculo.placa if despacho.vehiculo else "N/A"), estilos['dato']),
            Paragraph("Fecha:", estilos['etiqueta']),
            Paragraph(fecha_formateada, estilos['fecha'])
        ]

        fila2_data = [
            Paragraph("Guias:",  estilos['etiqueta']),
            Paragraph(str(despacho_detalles.count()), estilos['dato']),
            Paragraph("Peso:", estilos['etiqueta']),
            Paragraph(f"{int(despacho.peso)}" if despacho.peso else "0", estilos['dato']),
            Paragraph("Volumen:",  estilos['etiqueta']),
            Paragraph(f"{int(despacho.volumen)}" if despacho.volumen else "0", estilos['dato'])
        ]

        ancho_total = letter[0] - (0.8 * inch)
        anchos_columnas = [
            ancho_total * 0.15,
            ancho_total * 0.18,
            ancho_total * 0.15,
            ancho_total * 0.18,
            ancho_total * 0.12,
            ancho_total * 0.22,
        ]

        tabla_fila1 = Table([fila1_data], colWidths=anchos_columnas)
        tabla_fila2 = Table([fila2_data], colWidths=anchos_columnas)

        estilo_info_despacho = TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
        ])

        tabla_fila1.setStyle(estilo_info_despacho)
        tabla_fila2.setStyle(estilo_info_despacho)

        elementos.append(tabla_fila1)
        elementos.append(tabla_fila2)
        elementos.append(Spacer(1, 12))

        data = [["Id", "Guia", "Fecha", "Cliente", "Destinatario", "Dirección", "Und", "Peso"]]

        for detalle in despacho_detalles:
            fecha_formateada = detalle.guia.fecha.strftime("%Y-%m-%d") if detalle.guia.fecha else "N/A"

            id = Paragraph(str(detalle.id), estilos['tabla'])
            guia = Paragraph(str(detalle.guia_id), estilos['tabla'])
            fecha = Paragraph(str(fecha_formateada), estilos['tabla'])
            cliente = Paragraph(str(detalle.guia.cliente.nombre_corto), estilos['tabla'])
            destinatario = Paragraph(str(detalle.guia.destinatario_nombre), estilos['tabla'])
            destinatario_direccion = Paragraph(str(detalle.guia.destinatario_direccion), estilos['tabla'])
            peso = Paragraph(str(int(detalle.peso)) if detalle.peso is not None else "0", estilos['numero_tabla'])
            unidad = Paragraph(str(int(detalle.unidades)) if detalle.unidades is not None else "0", estilos['numero_tabla'])

            data.append([id, guia, fecha, cliente, destinatario, destinatario_direccion, peso, unidad])

        anchos_columnas_visitas = [
            ancho_total * 0.04,
            ancho_total * 0.06,
            ancho_total * 0.10,
            ancho_total * 0.20,
            ancho_total * 0.20,
            ancho_total * 0.30,
            ancho_total * 0.05,
            ancho_total * 0.05,
        ]

        table = Table(data, repeatRows=1, colWidths=anchos_columnas_visitas)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("ALIGN", (0, 1), (-1, -1), "LEFT"),
            ("ALIGN", (6, 1), (6, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 7),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("WORDWRAP", (0, 0), (-1, -1)),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        elementos.append(table)
        
        doc.build(
            elementos,
            onFirstPage=_encabezado,
            onLaterPages=_encabezado,
            canvasmaker=PDFUtilidades.PieDePagina
        )
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes