from django.db import models

class Cuenta(models.Model):    
    codigo = models.IntegerField(null=True)
    nombre = models.CharField(max_length=100, null=True)
    movimiento = models.BooleanField(default = False)
    requiere_tercero = models.BooleanField(default = False)
    requiere_centro_costo = models.BooleanField(default = False)

    class Meta:
        db_table = "con_cuenta"