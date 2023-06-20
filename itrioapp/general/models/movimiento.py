from django.db import models
from general.models.movimiento_tipo import MovimientoTipo
from general.models.contacto import Contacto
class Movimiento(models.Model):    
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
    movimiento_tipo = models.ForeignKey(MovimientoTipo, on_delete=models.CASCADE, related_name='movimientos')
    contacto = models.ForeignKey(Contacto, null=True, on_delete=models.CASCADE, related_name='movimientos')

    class Meta:
        db_table = "gen_movimiento"