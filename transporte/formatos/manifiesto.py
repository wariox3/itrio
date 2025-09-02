from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from general.formatos.encabezado import FormatoEncabezado
from reportlab.lib.units import inch
from utilidades.pdf_utilidades import PDFUtilidades
from transporte.models.despacho import TteDespacho
from transporte.models.despacho_detalle import TteDespachoDetalle
from reportlab.lib import colors


class FormatoManifiesto:
    def generar_pdf(self, despacho_id):
        buffer = BytesIO()
        
        # Configurar página en formato horizontal (landscape)
        ancho, alto = landscape(letter)  # Invierte las dimensiones de letter
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(letter),  # Usar landscape en lugar de letter
            leftMargin=0.4*inch, 
            rightMargin=0.4*inch,
            topMargin=0.5*inch, 
            bottomMargin=0.5*inch
        )
        
        elementos = []
        estilos = PDFUtilidades.obtener_estilos()

        elementos.append(Paragraph("Título del Manifiesto", estilos['titulo']))
        elementos.append(Spacer(1, 0.2*inch))
        
        doc.build(
            elementos,
            canvasmaker=PDFUtilidades.PieDePagina
        )
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes