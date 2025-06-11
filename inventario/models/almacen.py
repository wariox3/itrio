from django.db import models

class InvAlmacen(models.Model):        
    nombre = models.CharField(max_length=80)  

    class Meta:
        db_table = "inv_almacen"
        ordering = ["-id"]