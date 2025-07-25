from django.db import models

class ConMetodoDepreciacion(models.Model):    
    id = models.IntegerField(primary_key=True)    
    nombre = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "con_metodo_depreciacion"
        ordering = ["-id"]