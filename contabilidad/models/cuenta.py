from django.db import models

class Cuenta(models.Model):    
    codigo = models.IntegerField(null=True)
    nombre = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "con_cuenta"