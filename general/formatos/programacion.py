from humano.models.programacion import HumProgramacion
from humano.models.programacion_detalle import HumProgramacionDetalle

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from general.formatos.encabezado import FormatoEncabezado

class FormatoProgramacion():
    def __init__(self):
        self.encabezado = FormatoEncabezado()

    def generar_pdf(self, id):  
        buffer = BytesIO()   
        p = canvas.Canvas(buffer, pagesize=letter)                
        self.encabezado.generar_pdf(p, "PROGRAMACION DE NÓMINA")
        p.setFont("Helvetica", 10)        
        programacion = HumProgramacion.objects.filter(pk=id).values(
            'id', 'nombre', 'devengado', 'deduccion', 'total', 'fecha_desde', 'fecha_hasta'
            ).first()        
        programacion_detalles = HumProgramacionDetalle.objects.filter(programacion_id = id).values(
            'devengado', 'deduccion', 'total',
            'contrato__contacto__numero_identificacion',
            'contrato__contacto__nombre_corto',
            'contrato__contacto__numero_cuenta',
            'contrato__contacto__banco__nombre',
            )

        x = 40
        y = 680
        alto_fila = 15  
        tamano_texto_encabezado = 9   
        p.setFont("Helvetica-Bold", tamano_texto_encabezado)    
        p.drawString(40, y - alto_fila * 1, 'CODIGO')
        p.drawString(40, y - alto_fila * 2, 'DESDE')
        p.drawString(40, y - alto_fila * 3, 'HASTA')
        p.drawString(40, y - alto_fila * 4, '')
        p.setFont("Helvetica", tamano_texto_encabezado)
        p.drawString(110, y - alto_fila * 1, str(programacion['id']))
        p.drawString(110, y - alto_fila * 2, programacion['fecha_desde'].strftime('%Y-%m-%d'))
        p.drawString(110, y - alto_fila * 3, programacion['fecha_hasta'].strftime('%Y-%m-%d'))
        p.drawString(110, y - alto_fila * 4, '')    

        p.setFont("Helvetica-Bold", tamano_texto_encabezado) 
        p.drawString(270, y - alto_fila * 1, 'NOMBRE')
        p.drawString(270, y - alto_fila * 2, '')
        p.drawString(270, y - alto_fila * 3, '')
        p.drawString(270, y - alto_fila * 4, '')
        p.setFont("Helvetica", tamano_texto_encabezado)
        p.drawString(370, y - alto_fila * 1, programacion['nombre'] or "")
        p.drawString(370, y - alto_fila * 2, '')
        p.drawString(370, y - alto_fila * 3, '')
        p.drawString(370, y - alto_fila * 4, '')  

        p.setFont("Helvetica-Bold", tamano_texto_encabezado) 
        p.drawString(460, y - alto_fila * 1, 'DEVENGADO')
        p.drawString(460, y - alto_fila * 2, 'DEDUCCION')
        p.drawString(460, y - alto_fila * 3, 'TOTAL')
        p.drawString(460, y - alto_fila * 4, '')
        p.setFont("Helvetica", tamano_texto_encabezado)
        p.drawString(520, y - alto_fila * 1, f"{programacion['devengado']:,.0f}")
        p.drawString(520, y - alto_fila * 2, f"{programacion['deduccion']:,.0f}")
        p.drawString(520, y - alto_fila * 3, f"{programacion['total']:,.0f}")
        p.drawString(520, y - alto_fila * 4, '')         

        y = 580
        margen = 2
        ancho_columna = [70, 150, 70, 60, 60, 60, 60]  

        p.setFont("Helvetica-Bold", 8)                 
        p.drawString(x + sum(ancho_columna[:0]) + margen, y + 4, 'IDENTIFICACION')
        p.drawString(x + sum(ancho_columna[:1]) + margen, y + 4, 'EMPLEADO')
        p.drawString(x + sum(ancho_columna[:2]) + margen, y + 4, 'CUENTA')            
        p.drawString(x + sum(ancho_columna[:3]) + margen, y + 4, 'BANCO')
        p.drawString(x + sum(ancho_columna[:4]) + margen, y + 4, 'DEVENGADO')
        p.drawString(x + sum(ancho_columna[:5]) + margen, y + 4, 'DEDUCCION')
        p.drawString(x + sum(ancho_columna[:6]) + margen, y + 4, 'TOTAL')
        
        for i in range(7):
            p.rect(x + sum(ancho_columna[:i]), y, ancho_columna[i], alto_fila)
        y -= alto_fila

        p.setFont("Helvetica", 8)
        for programacion_detalle in programacion_detalles:      
            y_texto = y + 5
            p.drawString(x + sum(ancho_columna[:0]) + margen, y_texto, str(programacion_detalle['contrato__contacto__numero_identificacion']))
            p.drawString(x + sum(ancho_columna[:1]) + margen, y_texto, str(programacion_detalle['contrato__contacto__nombre_corto']))
            p.drawString(x + sum(ancho_columna[:2]) + margen, y_texto, str(programacion_detalle['contrato__contacto__numero_cuenta'] or ""))            
            p.drawString(x + sum(ancho_columna[:3]) + margen, y_texto, str(programacion_detalle['contrato__contacto__banco__nombre'] or ""))                        
            p.drawRightString(x + sum(ancho_columna[:4]) + ancho_columna[4] - margen, y_texto, f"{programacion_detalle['devengado']:,.0f}")
            p.drawRightString(x + sum(ancho_columna[:5]) + ancho_columna[5] - margen, y_texto, f"{programacion_detalle['deduccion']:,.0f}")
            p.drawRightString(x + sum(ancho_columna[:6]) + ancho_columna[6] - margen, y_texto, f"{programacion_detalle['total']:,.0f}")

            for i in range(7):
                p.rect(x + sum(ancho_columna[:i]), y, ancho_columna[i], alto_fila)
            y -= alto_fila    

        p.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
