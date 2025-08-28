from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from general.formatos.encabezado import FormatoEncabezado
from ruteo.models.visita import RutVisita 


class FormatoOrdenEntrega:
    def __init__(self):
        self.encabezado = FormatoEncabezado()

    def generar_pdf(self, despacho_id):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elementos = []
        estilos = getSampleStyleSheet()

        # Encabezado (si quieres integrarlo con Platypus)
        elementos.append(Paragraph("<b>ORDEN DE ENTREGA</b>", estilos["Title"]))
        elementos.append(Spacer(1, 12))

        # Obtener visitas
        visitas = RutVisita.objects.filter(despacho_id=despacho_id)

        if not visitas.exists():
            elementos.append(Paragraph("No hay visitas registradas.", estilos["Normal"]))
        else:
            # Definir datos de tabla
            data = [["#", "Cliente", "Dirección", "Fecha", "Estado"]]
            for i, visita in enumerate(visitas, start=1):
                data.append([
                    i,
                    str(visita.numero),     # Ajusta a tus campos reales
                    # str(visita.direccion),   # Ajusta
                    # visita.fecha.strftime("%d/%m/%Y") if visita.fecha else "",
                    # str(visita.estado)       # Ajusta
                ])

            # Crear tabla
            table = Table(data, repeatRows=1)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ]))
            elementos.append(table)

        # Construir PDF
        doc.build(elementos)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
