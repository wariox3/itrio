from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from general.formatos.encabezado import FormatoEncabezado

class FormatoRecibo():
    def __init__(self):
        self.encabezado = FormatoEncabezado()

    def generar_pdf(self, id):  
        buffer = BytesIO()   
        p = canvas.Canvas(buffer, pagesize=letter)  
        p.setTitle("recibo_de_caja")              

        # Encabezado del documento
        self.encabezado.generar_pdf(p, "RECIBO DE CAJA")
        p.setFont("Helvetica", 8) 

        # Obtener datos del documento
        documento = GenDocumento.objects.filter(pk=id).values(
            'numero', 'total', 'fecha', 
            'contacto__nombre_corto', 'contacto__numero_identificacion'
        ).first()        

        # Obtener los detalles del documento
        documento_detalles = GenDocumentoDetalle.objects.filter(documento_id=id).values(
            'numero', 'contacto__numero_identificacion', 'contacto__nombre_corto', 
            'cuenta__nombre', 'cuenta__codigo', 'naturaleza', 'pago'
        )

        # Primera tabla: Información del documento
        y = 660  # Comienza en la parte superior de la página

        # Estilo para los encabezados
        p.setFont("Helvetica-Bold", 9)
        # Número y Contacto
        p.drawString(30, y, "NUMERO:")
        p.setFont("Helvetica", 8)
        p.drawString(80, y, str(documento['numero'] or ''))

        p.setFont("Helvetica-Bold", 9)
        p.drawString(180, y, "CONTACTO:")
        p.setFont("Helvetica", 8)
        p.drawString(240, y, f"{documento['contacto__numero_identificacion'] or ''} - {documento['contacto__nombre_corto'][:58] or ''}")

        # Fecha
        y -= 20
        p.setFont("Helvetica-Bold", 9)
        p.drawString(30, y, "FECHA:")
        p.setFont("Helvetica", 8)
        p.drawString(80, y, documento['fecha'].strftime('%Y-%m-%d') if documento['fecha'] else '')

        # Total alineado a la derecha
        p.setFont("Helvetica-Bold", 9)
        p.drawString(180, y, "TOTAL:")
        p.setFont("Helvetica", 8)
        p.drawRightString(240, y, f"{documento['total'] or 0}")


        # Segunda tabla: Detalles del documento
        y -= 40  # Dejar espacio entre las tablas
        p.setFont("Helvetica-Bold", 9)
        p.drawString(30, y, 'NUMERO')
        p.drawString(80, y, 'CONTACTO')
        p.drawString(300, y, 'CUENTA')
        p.drawString(420, y, 'NATURALEZA')
        p.drawString(500, y, 'PAGO')

        p.setFont("Helvetica", 8)
        y -= 20
        for detalle in documento_detalles:
            p.drawString(30, y, str(detalle['numero'] or ''))
            p.drawString(80, y, (detalle['contacto__nombre_corto'][:40] or '') if detalle['contacto__nombre_corto'] else '')
            p.drawString(300, y, f"{detalle['cuenta__codigo'] or ''} - {detalle['cuenta__nombre'][:40] or ''}")
            p.drawString(420, y, detalle['naturaleza'] or '')
            p.drawString(520, y, f"{detalle['pago']:.2f}" if detalle['pago'] else '')
            y -= 20  # Reducir la altura entre filas

            if y < 100:  # Si se alcanza el final de la página, añadir una nueva página
                p.showPage()
                y = 750
                p.setFont("Helvetica-Bold", 9)
                p.drawString(30, y, 'Numero')
                p.drawString(80, y, 'Nombre Contacto')
                p.drawString(300, y, 'Cuenta')
                p.drawString(420, y, 'Naturaleza')
                p.drawString(520, y, 'Pago')
                p.setFont("Helvetica", 8)
                y -= 20


        p.save()

        # Obtener los bytes del PDF
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
