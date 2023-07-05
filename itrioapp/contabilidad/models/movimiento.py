from django.db import models

class Movimiento(models.Model):    
    numero = models.IntegerField(null=True)
    fecha = models.DateField(null=True)
    debito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    base = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "con_movimiento"