from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from general.formatos.encabezado import FormatoEncabezado

class FormatoDocumentoSoporte():
    def __init__(self):
        self.encabezado = FormatoEncabezado()

    def generar_pdf(self, id):  
        buffer = BytesIO()   
        p = canvas.Canvas(buffer, pagesize=letter)                
        self.encabezado.generar_pdf(p, "DOCUMENTO SOPORTE")
        p.setFont("Helvetica", 10)        
        documento = GenDocumento.objects.filter(pk=id).values(
            'numero', 'fecha', 'fecha_vence', 'total',
            'contacto__nombre_corto',
            'contacto__numero_identificacion'        
            ).first()        
        documento_detalles = GenDocumentoDetalle.objects.filter(documento_id = id).values(
            'item_id', 'cantidad', 'precio', 'total',
            'item__nombre',
            'item__referencia')

        x = 40
        y = 680
        alto_fila = 15  
        tamano_texto_encabezado = 9   
        p.setFont("Helvetica-Bold", tamano_texto_encabezado)    
        p.drawString(40, y - alto_fila * 1, 'NUMERO')
        p.drawString(40, y - alto_fila * 2, 'NIT')
        p.drawString(40, y - alto_fila * 3, 'PROVEEDOR')
        p.drawString(40, y - alto_fila * 4, '')
        p.setFont("Helvetica", tamano_texto_encabezado)
        p.drawString(110, y - alto_fila * 1, str(documento['numero']))
        p.drawString(110, y - alto_fila * 2, documento['contacto__numero_identificacion'])
        p.drawString(110, y - alto_fila * 3, documento['contacto__nombre_corto'])
        p.drawString(110, y - alto_fila * 4, '')      

        p.setFont("Helvetica-Bold", tamano_texto_encabezado) 
        p.drawString(270, y - alto_fila * 1, 'FECHA')
        p.drawString(270, y - alto_fila * 2, 'VENCE')
        p.drawString(270, y - alto_fila * 3, '')
        p.drawString(270, y - alto_fila * 4, '')
        p.setFont("Helvetica", tamano_texto_encabezado)
        p.drawString(370, y - alto_fila * 1, documento['fecha'].strftime('%Y-%m-%d'))
        p.drawString(370, y - alto_fila * 2, documento['fecha_vence'].strftime('%Y-%m-%d'))
        p.drawString(370, y - alto_fila * 3, '')
        p.drawString(370, y - alto_fila * 4, '') 

        p.setFont("Helvetica-Bold", tamano_texto_encabezado) 
        p.drawString(460, y - alto_fila * 1, 'TOTAL')
        p.drawString(460, y - alto_fila * 2, '')
        p.drawString(460, y - alto_fila * 3, '')
        p.drawString(460, y - alto_fila * 4, '')
        p.setFont("Helvetica", tamano_texto_encabezado)
        p.drawString(510, y - alto_fila * 1, f"{documento['total']:,.0f}")
        p.drawString(510, y - alto_fila * 2, '')
        p.drawString(510, y - alto_fila * 3, '')
        p.drawString(510, y - alto_fila * 4, '')

        y = 580
        margen = 2
        ancho_columna = [30, 230, 80, 50, 70, 70]  

        p.setFont("Helvetica-Bold", 8)                 
        p.drawString(x + sum(ancho_columna[:0]) + margen, y + 4, 'COD')
        p.drawString(x + sum(ancho_columna[:1]) + margen, y + 4, 'ITEM')
        p.drawString(x + sum(ancho_columna[:2]) + margen, y + 4, 'REF')            
        p.drawString(x + sum(ancho_columna[:3]) + margen, y + 4, 'CANT')
        p.drawString(x + sum(ancho_columna[:4]) + margen, y + 4, 'PRECIO')
        p.drawString(x + sum(ancho_columna[:5]) + margen, y + 4, 'TOTAL')
        for i in range(6):
            p.rect(x + sum(ancho_columna[:i]), y, ancho_columna[i], alto_fila)
        y -= alto_fila

        p.setFont("Helvetica", 8)
        for documento_detalle in documento_detalles:      
            y_texto = y + 5
            p.drawString(x + sum(ancho_columna[:0]) + margen, y_texto, str(documento_detalle['item_id']))
            p.drawString(x + sum(ancho_columna[:1]) + margen, y_texto, str(documento_detalle['item__nombre']))
            p.drawString(x + sum(ancho_columna[:2]) + margen, y_texto, str(documento_detalle['item__referencia'] or ""))            
            p.drawRightString(x + sum(ancho_columna[:3]) + ancho_columna[3] - margen, y_texto, f"{documento_detalle['cantidad']:.2f}")
            p.drawRightString(x + sum(ancho_columna[:4]) + ancho_columna[4] - margen, y_texto, f"{documento_detalle['precio']:,.0f}")
            p.drawRightString(x + sum(ancho_columna[:5]) + ancho_columna[5] - margen, y_texto, f"{documento_detalle['total']:,.0f}")
            for i in range(6):
                p.rect(x + sum(ancho_columna[:i]), y, ancho_columna[i], alto_fila)
            y -= alto_fila
        
        '''p.setFont("Helvetica-Bold", tamano_texto_encabezado)
        p.drawString(400, y - alto_fila * 1, 'TOTAL DEVENGADO')        
        p.drawString(400, y - alto_fila * 2, 'TOTAL DEDUCCIONES')        
        p.drawString(400, y - alto_fila * 3, 'NETO A PAGAR')        
        p.setFont("Helvetica", tamano_texto_encabezado)
        p.drawRightString(570, y - alto_fila * 1, f"{documento['devengado']:,.0f}")        
        p.drawRightString(570, y - alto_fila * 2, f"{documento['deduccion']:,.0f}")        
        p.drawRightString(570, y - alto_fila * 3, f"{documento['total']:,.0f}")        
        y -= alto_fila * 3'''

        p.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
