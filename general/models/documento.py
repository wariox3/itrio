from django.db import models
from general.models.documento_tipo import GenDocumentoTipo
from general.models.contacto import GenContacto
from general.models.metodo_pago import GenMetodoPago
from general.models.resolucion import GenResolucion
from general.models.empresa import GenEmpresa
from general.models.plazo_pago import GenPlazoPago
from general.models.gen_asesor import GenAsesor
from general.models.sede import GenSede
from seguridad.models import User
from decimal import Decimal, ROUND_HALF_UP

class GenDocumento(models.Model):    
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
    documento_tipo = models.ForeignKey(GenDocumentoTipo, on_delete=models.PROTECT, related_name='gen_documentos')
    contacto = models.ForeignKey(GenContacto, null=True, on_delete=models.PROTECT, related_name='contactos_rel')
    metodo_pago = models.ForeignKey(GenMetodoPago, null=True, on_delete=models.PROTECT, related_name='gen_documentos')
    resolucion = models.ForeignKey(GenResolucion, null=True, on_delete=models.PROTECT, related_name='gen_documentos')
    empresa = models.ForeignKey(GenEmpresa, on_delete=models.PROTECT, related_name='gen_documentos')
    documento_referencia = models.ForeignKey('self', null=True, on_delete=models.PROTECT, related_name='gen_documentos')
    plazo_pago = models.ForeignKey(GenPlazoPago, null=True, on_delete=models.PROTECT,related_name='gen_documentos')
    asesor = models.ForeignKey(GenAsesor, null=True, on_delete=models.PROTECT,related_name='documentos_asesor_rel')
    sede = models.ForeignKey(GenSede, null=True, on_delete=models.PROTECT,related_name='documentos_sede_rel')
    usuario = models.ForeignKey(User, null=True, on_delete=models.PROTECT,related_name='documentos_usuario_rel')

    class Meta:
        db_table = "gen_documento"