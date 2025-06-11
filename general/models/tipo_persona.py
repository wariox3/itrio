from django.db import models

class GenTipoPersona(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    
    class Meta:
        db_table = "gen_tipo_persona"
        ordering = ["-id"]