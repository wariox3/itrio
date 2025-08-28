from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from general.formatos.encabezado import FormatoEncabezado
from ruteo.models.visita import RutVisita 
from ruteo.models.despacho import RutDespacho
from reportlab.lib.units import inch

class FormatoOrdenEntrega:
    def generar_pdf(self, despacho_id):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, 
                               leftMargin=30, rightMargin=30,
                               topMargin=120, bottomMargin=30)
        elementos = []
        estilos = getSampleStyleSheet()

        def _encabezado(canvas, doc):
            FormatoEncabezado().generar_pdf(canvas, "ORDEN DE ENTREGA")

        try:
            despacho = RutDespacho.objects.get(id=despacho_id)
        except RutDespacho.DoesNotExist:
            elementos.append(Paragraph("Despacho no encontrado.", estilos["Normal"]))
            doc.build(elementos, onFirstPage=_encabezado, onLaterPages=_encabezado)
            pdf_bytes = buffer.getvalue()
            buffer.close()
            return pdf_bytes

        visitas = RutVisita.objects.filter(despacho_id=despacho_id)

        estilo_etiqueta = getSampleStyleSheet()["Normal"]
        estilo_etiqueta.fontName = "Helvetica-Bold"
        estilo_etiqueta.fontSize = 9
        estilo_etiqueta.leading = 11
        
        estilo_dato = getSampleStyleSheet()["Normal"]
        estilo_dato.fontName = "Helvetica"
        estilo_dato.fontSize = 9
        estilo_dato.leading = 11
        
        fila1_data = [
            Paragraph("ID Despacho:", estilo_etiqueta),
            Paragraph(str(despacho.id), estilo_dato),
            Paragraph("Vehículo:", estilo_etiqueta),
            Paragraph(str(despacho.vehiculo.placa if despacho.vehiculo else "N/A"), estilo_dato),
            Paragraph("Fecha:", estilo_etiqueta),
            Paragraph(str(despacho.fecha), estilo_dato)
        ]

        fila2_data = [
            Paragraph("Peso Total:", estilo_etiqueta),
            Paragraph(f"{despacho.peso or 0:.2f} kg" if despacho.peso else "0 kg", estilo_dato),
            Paragraph("Volumen Total:", estilo_etiqueta),
            Paragraph(f"{despacho.volumen or 0:.2f}" if despacho.volumen else "0", estilo_dato),
            Paragraph("Total Visitas:", estilo_etiqueta),
            Paragraph(str(visitas.count()), estilo_dato)
        ]

        ancho_total = letter[0] - 60
        anchos_columnas = [
            ancho_total * 0.12,
            ancho_total * 0.18,
            ancho_total * 0.12,
            ancho_total * 0.18,
            ancho_total * 0.12,
            ancho_total * 0.18,
        ]

        tabla_fila1 = Table([fila1_data], colWidths=anchos_columnas)
        tabla_fila2 = Table([fila2_data], colWidths=anchos_columnas)

        estilo_info_despacho = TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
        ])

        tabla_fila1.setStyle(estilo_info_despacho)
        tabla_fila2.setStyle(estilo_info_despacho)

        elementos.append(tabla_fila1)
        elementos.append(tabla_fila2)
        elementos.append(Spacer(1, 15))

        if not visitas.exists():
            elementos.append(Paragraph("No hay visitas registradas.", estilos["Normal"]))
        else:
            data = [["Id", "Numero", "Documento", "Destinatario", "Dirección", "Peso"]]
            
            # Estilo para datos de visitas
            estilo_normal = getSampleStyleSheet()["Normal"]
            estilo_normal.fontName = "Helvetica"
            estilo_normal.fontSize = 8
            estilo_normal.leading = 10
            
            # Estilo especial para números alineados a la derecha
            estilo_numero = getSampleStyleSheet()["Normal"]
            estilo_numero.fontName = "Helvetica"
            estilo_numero.fontSize = 8
            estilo_numero.alignment = 2
            
            for visita in visitas:
                id = Paragraph(str(visita.id), estilo_normal)
                numero = Paragraph(str(visita.numero), estilo_normal)
                documento = Paragraph(str(visita.documento), estilo_normal)
                destinatario = Paragraph(str(visita.destinatario), estilo_normal)
                direccion = Paragraph(str(visita.destinatario_direccion), estilo_normal)
                
                peso_formateado = str(int(visita.peso)) if visita.peso else "0"
                peso = Paragraph(peso_formateado, estilo_numero)
                
                data.append([id, numero, documento, destinatario, direccion, peso])

            # Calcular anchos de columna proporcionales para la tabla de visitas
            anchos_columnas_visitas = [
                ancho_total * 0.05,
                ancho_total * 0.10,
                ancho_total * 0.15,
                ancho_total * 0.25,
                ancho_total * 0.35,
                ancho_total * 0.07, 
            ]

            table = Table(data, repeatRows=1, colWidths=anchos_columnas_visitas)
            
            table.setStyle(TableStyle([
                # Estilo para encabezado de tabla - USANDO EL MISMO COLOR QUE EL ENCABEZADO
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),  # Cambiado a lightgrey
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),  # Cambiado a negro para mejor contraste
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("ALIGN", (2, 1), (3, -1), "LEFT"),
                ("ALIGN", (5, 1), (5, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                
                # Fuentes
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("WORDWRAP", (0, 0), (-1, -1)),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ]))
            elementos.append(table)

        doc.build(elementos, onFirstPage=_encabezado, onLaterPages=_encabezado)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes