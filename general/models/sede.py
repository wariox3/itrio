from django.db import models
from contabilidad.models.grupo import ConGrupo

class GenSede(models.Model):        
    nombre = models.CharField(max_length=100)
    grupo = models.ForeignKey(ConGrupo, null=True, on_delete=models.PROTECT, related_name='sedes_grupo_rel')

    class Meta:
        db_table = "gen_sede"