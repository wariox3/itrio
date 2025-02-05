from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from general.formatos.encabezado import FormatoEncabezado
from utilidades.utilidades import Utilidades
class FormatoNomina():
    def __init__(self):
        self.encabezado = FormatoEncabezado()

    def generar_pdf(self, id):  
        buffer = BytesIO()   
        p = canvas.Canvas(buffer, pagesize=letter)  
        p.setTitle("nomina")              
        self.encabezado.generar_pdf(p, "COMPROBANTE DE PAGO NÓMINA")
        p.setFont("Helvetica", 10)        
        documento = GenDocumento.objects.filter(pk=id).values(
            'numero', 'deduccion', 'devengado', 'total', 'fecha', 'fecha_hasta', 
            'contacto__nombre_corto',
            'contacto__numero_identificacion',
            'contacto__numero_cuenta',
            'contacto__banco__nombre',
            'periodo__nombre', 
            'salario',
            'contrato__cargo__nombre', 
            'contrato__grupo__nombre'
            ).first()        
        documento_detalles = GenDocumentoDetalle.objects.filter(documento_id = id).values(
            'concepto_id', 'concepto__nombre', 'detalle', 'cantidad', 'dias', 'porcentaje', 'devengado', 'deduccion')

        x = 40
        y = 680
        alto_fila = 15  
        tamano_texto_encabezado = 9   
        p.setFont("Helvetica-Bold", tamano_texto_encabezado)    
        p.drawString(40, y - alto_fila * 1, 'NUMERO')
        p.drawString(40, y - alto_fila * 2, 'EMPLEADO')
        p.drawString(40, y - alto_fila * 3, 'CARGO')
        p.drawString(40, y - alto_fila * 4, 'GRUPO')
        p.setFont("Helvetica", tamano_texto_encabezado)
        p.drawString(110, y - alto_fila * 1, str(documento['numero']) if documento['numero'] is not None else '0')
        p.drawString(110, y - alto_fila * 2, Utilidades.pdf_texto(documento['contacto__nombre_corto'], 30))
        p.drawString(110, y - alto_fila * 3, documento['contrato__cargo__nombre'])
        p.drawString(110, y - alto_fila * 4, documento['contrato__grupo__nombre'])    

        p.setFont("Helvetica-Bold", tamano_texto_encabezado) 
        p.drawString(270, y - alto_fila * 1, 'PERIODO')
        p.drawString(270, y - alto_fila * 2, 'IDENTIFICACION')
        p.drawString(270, y - alto_fila * 3, 'DESDE')
        p.drawString(270, y - alto_fila * 4, 'HASTA')
        p.setFont("Helvetica", tamano_texto_encabezado)
        p.drawString(370, y - alto_fila * 1, documento['periodo__nombre'])
        p.drawString(370, y - alto_fila * 2, documento['contacto__numero_identificacion'])
        p.drawString(370, y - alto_fila * 3, documento['fecha'].strftime('%Y-%m-%d'))
        p.drawString(370, y - alto_fila * 4, documento['fecha_hasta'].strftime('%Y-%m-%d'))  

        p.setFont("Helvetica-Bold", tamano_texto_encabezado) 
        p.drawString(460, y - alto_fila * 1, 'CUENTA')
        p.drawString(460, y - alto_fila * 2, 'BANCO')
        p.drawString(460, y - alto_fila * 3, 'SALARIO')
        p.drawString(460, y - alto_fila * 4, '')
        p.setFont("Helvetica", tamano_texto_encabezado)
        p.drawString(510, y - alto_fila * 1, str(documento.get('contacto__numero_cuenta') or ''))
        p.drawString(510, y - alto_fila * 2, str(documento.get('contacto__banco__nombre') or ''))
        p.drawString(510, y - alto_fila * 3, f"{documento['salario']:,.0f}")
        p.drawString(510, y - alto_fila * 4, '')  


        y = 580
        margen = 2
        ancho_columna = [30, 180, 130, 35, 30, 20, 55, 55]  

        p.setFont("Helvetica-Bold", 8)                 
        p.drawString(x + sum(ancho_columna[:0]) + margen, y + 4, 'COD')
        p.drawString(x + sum(ancho_columna[:1]) + margen, y + 4, 'CONCEPTO')
        p.drawString(x + sum(ancho_columna[:2]) + margen, y + 4, 'DETALLE')            
        p.drawString(x + sum(ancho_columna[:3]) + margen, y + 4, 'HORAS')
        p.drawString(x + sum(ancho_columna[:4]) + margen, y + 4, 'DÍAS')
        p.drawString(x + sum(ancho_columna[:5]) + margen, y + 4, '%')
        p.drawString(x + sum(ancho_columna[:6]) + margen, y + 4, 'DEVENGADO')
        p.drawString(x + sum(ancho_columna[:7]) + margen, y + 4, 'DEDUCCION')
        for i in range(8):
            p.rect(x + sum(ancho_columna[:i]), y, ancho_columna[i], alto_fila)
        y -= alto_fila

        p.setFont("Helvetica", 8)
        for documento_detalle in documento_detalles:      
            y_texto = y + 5
            p.drawString(x + sum(ancho_columna[:0]) + margen, y_texto, str(documento_detalle['concepto_id']))
            p.drawString(x + sum(ancho_columna[:1]) + margen, y_texto, str(documento_detalle['concepto__nombre']))
            p.drawString(x + sum(ancho_columna[:2]) + margen, y_texto, Utilidades.pdf_texto(documento_detalle['detalle'], 36))            
            p.drawRightString(x + sum(ancho_columna[:3]) + ancho_columna[3] - margen, y_texto, f"{documento_detalle['cantidad']:.2f}")
            p.drawRightString(x + sum(ancho_columna[:4]) + ancho_columna[4] - margen, y_texto, str(int(documento_detalle['dias'])))
            p.drawRightString(x + sum(ancho_columna[:5]) + ancho_columna[5] - margen, y_texto, str(int(documento_detalle['porcentaje'])))
            p.drawRightString(x + sum(ancho_columna[:6]) + ancho_columna[6] - margen, y_texto, f"{documento_detalle['devengado']:,.0f}")
            p.drawRightString(x + sum(ancho_columna[:7]) + ancho_columna[7] - margen, y_texto, f"{documento_detalle['deduccion']:,.0f}")
            for i in range(8):
                p.rect(x + sum(ancho_columna[:i]), y, ancho_columna[i], alto_fila)
            y -= alto_fila
        
        p.setFont("Helvetica-Bold", tamano_texto_encabezado)
        p.drawString(400, y - alto_fila * 1, 'TOTAL DEVENGADO')        
        p.drawString(400, y - alto_fila * 2, 'TOTAL DEDUCCIONES')        
        p.drawString(400, y - alto_fila * 3, 'NETO A PAGAR')        
        p.setFont("Helvetica", tamano_texto_encabezado)
        p.drawRightString(570, y - alto_fila * 1, f"{documento['devengado']:,.0f}")        
        p.drawRightString(570, y - alto_fila * 2, f"{documento['deduccion']:,.0f}")        
        p.drawRightString(570, y - alto_fila * 3, f"{documento['total']:,.0f}")        
        y -= alto_fila * 3

        p.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
