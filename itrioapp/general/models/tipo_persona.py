from django.db import models

class TipoPersona(models.Model):
    id = models.CharField(primary_key=True, max_length=2)
    nombre = models.CharField(max_length=30)
    
    class Meta:
        db_table = "gen_tipo_persona"