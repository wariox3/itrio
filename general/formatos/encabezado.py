from general.models.empresa import GenEmpresa
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from decouple import config

class FormatoEncabezado():

    def generar_pdf(self, p, titulo):
        region = config('DO_REGION')
        bucket = config('DO_BUCKET')  
        empresa = GenEmpresa.objects.get(pk=1)
        
        logo_url = f'https://{bucket}.{region}.digitaloceanspaces.com/{empresa.imagen}'
        try:
            logo = ImageReader(logo_url)
            p.drawImage(logo, 10, 680, width=100, height=100, mask='auto')
        except Exception as e:
            pass
        p.setFillColor(colors.lightgrey)
        p.rect(120, 757, 450, 17, stroke=0, fill=1)        
        p.setFillColor(colors.black)        
        p.setFont("Helvetica-Bold", 10)        
        p.drawCentredString(350,760, titulo)        
        p.drawString(120,740, empresa.nombre_corto or "")
        p.setFont("Helvetica", 10)
        nit = empresa.numero_identificacion or ""
        p.drawString(120,725, f"NIT {nit}")
        p.drawString(120,710, empresa.direccion or "")
        telefono = empresa.telefono or ""
        p.drawString(120,695, f"TEL {telefono}")        

    
