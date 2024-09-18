from django.db import models
from humano.models.periodo import HumPeriodo

class HumGrupo(models.Model):        
    nombre = models.CharField(max_length=100) 
    periodo = models.ForeignKey(HumPeriodo, on_delete=models.PROTECT, null=True, related_name='grupos_periodo_rel')

    class Meta:
        db_table = "hum_grupo"