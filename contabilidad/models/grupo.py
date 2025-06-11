from django.db import models

class ConGrupo(models.Model):        
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, default="0", unique=True)
    
    class Meta:
        db_table = "con_grupo"
        ordering = ["-id"]