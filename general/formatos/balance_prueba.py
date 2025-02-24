from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from general.formatos.encabezado import FormatoEncabezado
from reportlab.lib.enums import TA_LEFT
from datetime import datetime


class FormatoBalancePrueba:
    def __init__(self):
        self.encabezado = FormatoEncabezado()

    def generar_pdf(self, fecha_desde, fecha_hasta, resultados_json):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle("Informe Balance de Prueba")

        # Configuración general
        line_height = 20
        margin_top = 680
        margin_left = 30
        current_y = margin_top

        # Función para dibujar encabezados
        def draw_headers(pdf, current_y):
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawString(margin_left, current_y, "Código")
            pdf.drawString(margin_left + 60, current_y, "Nombre")
            pdf.drawString(margin_left + 260, current_y, "Anterior")
            pdf.drawString(margin_left + 340, current_y, "Débito")
            pdf.drawString(margin_left + 420, current_y, "Crédito")
            pdf.drawString(margin_left + 500, current_y, "Actual")

        # Título inicial
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(50, 750, "Balance de Prueba")
        pdf.setFont("Helvetica", 8)
        pdf.drawString(50, 730, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        pdf.drawString(50, 710, f"Periodo: {fecha_desde} a {fecha_hasta}")

        # Dibujar encabezados iniciales
        draw_headers(pdf, current_y)
        current_y -= line_height

        # Iterar resultados y generar contenido
        pdf.setFont("Helvetica", 8)
        for i, resultado in enumerate(resultados_json):
            if current_y < 50:  # Crear nueva página si no hay suficiente espacio
                pdf.showPage()
                pdf.setFont("Helvetica-Bold", 9)
                pdf.drawString(50, 750, "Balance de Prueba")
                pdf.setFont("Helvetica", 8)
                pdf.drawString(50, 730, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                pdf.drawString(50, 710, f"Periodo: {fecha_desde} a {fecha_hasta}")

                # Dibujar encabezados en la nueva página
                draw_headers(pdf, margin_top)
                current_y = margin_top - line_height

            # Dibujar contenido de cada fila
            pdf.setFont("Helvetica", 8)
            pdf.drawString(margin_left, current_y, str(resultado['codigo']))
            pdf.drawString(margin_left + 60, current_y, resultado['nombre'][:30])
            pdf.drawRightString(margin_left + 305, current_y, f"{resultado['saldo_anterior']:,.2f}")
            pdf.drawRightString(margin_left + 385, current_y, f"{resultado['debito']:,.2f}")
            pdf.drawRightString(margin_left + 465, current_y, f"{resultado['credito']:,.2f}")
            pdf.drawRightString(margin_left + 545, current_y, f"{resultado['saldo_actual']:,.2f}")
            current_y -= line_height

        # Finalizar el PDF
        pdf.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
