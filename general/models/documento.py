from django.db import models
from general.models.documento_tipo import DocumentoTipo
from general.models.contacto import Contacto
from general.models.metodo_pago import MetodoPago

class Documento(models.Model):    
    numero = models.IntegerField(null=True)
    fecha = models.DateField(null=True)
    fecha_contable = models.DateField(null=True)
    fecha_vence = models.DateField(null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    base_impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado_aprobado = models.BooleanField(default = False)
    documento_tipo = models.ForeignKey(DocumentoTipo, on_delete=models.CASCADE, related_name='gen_documentos')
    contacto = models.ForeignKey(Contacto, null=True, on_delete=models.CASCADE, related_name='gen_documentos')
    metodo_pago = models.ForeignKey(MetodoPago, null=True, on_delete=models.CASCADE, related_name='gen_documentos')
    
    class Meta:
        db_table = "gen_documento"