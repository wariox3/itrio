from django.db import models
from general.models.documento_tipo import DocumentoTipo
from general.models.contacto import Contacto
from general.models.metodo_pago import MetodoPago
from general.models.resolucion import Resolucion
from general.models.empresa import Empresa
from general.models.plazo_pago import PlazoPago
from general.models.asesor import Asesor
from general.models.sede import Sede
from seguridad.models import User
from decimal import Decimal, ROUND_HALF_UP

class Documento(models.Model):    
    numero = models.IntegerField(null=True)
    fecha = models.DateField(null=True)
    fecha_contable = models.DateField(null=True)
    fecha_vence = models.DateField(null=True)
    fecha_validacion = models.DateTimeField(null=True)
    subtotal = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    total_bruto = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    base_impuesto = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    descuento = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    impuesto = models.DecimalField(max_digits=20, decimal_places=6, default=0)    
    afectado = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    pendiente = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    estado_aprobado = models.BooleanField(default = False)
    estado_anulado = models.BooleanField(default = False)
    estado_electronico = models.BooleanField(default = False)    
    estado_electronico_enviado = models.BooleanField(default = False)    
    estado_electronico_notificado = models.BooleanField(default = False)    
    orden_compra = models.CharField(max_length=50,null=True)
    cue = models.CharField(max_length=150, null=True)
    soporte = models.CharField(max_length=100, null=True)
    comentario = models.CharField(max_length=500, null=True)
    qr = models.CharField(max_length=500, null=True)
    electronico_id = models.IntegerField(null=True)
    documento_tipo = models.ForeignKey(DocumentoTipo, on_delete=models.PROTECT, related_name='gen_documentos')
    contacto = models.ForeignKey(Contacto, null=True, on_delete=models.PROTECT, related_name='contactos_rel')
    metodo_pago = models.ForeignKey(MetodoPago, null=True, on_delete=models.PROTECT, related_name='gen_documentos')
    resolucion = models.ForeignKey(Resolucion, null=True, on_delete=models.PROTECT, related_name='gen_documentos')
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='gen_documentos')
    documento_referencia = models.ForeignKey('self', null=True, on_delete=models.PROTECT, related_name='gen_documentos')
    plazo_pago = models.ForeignKey(PlazoPago, null=True, on_delete=models.PROTECT,related_name='gen_documentos')
    asesor = models.ForeignKey(Asesor, null=True, on_delete=models.PROTECT,related_name='documentos_asesor_rel')
    sede = models.ForeignKey(Sede, null=True, on_delete=models.PROTECT,related_name='documentos_sede_rel')
    usuario = models.ForeignKey(User, null=True, on_delete=models.PROTECT,related_name='documentos_usuario_rel')

    class Meta:
        db_table = "gen_documento"