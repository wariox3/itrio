from django.db import models

class HumGrupo(models.Model):        
    nombre = models.CharField(max_length=100)    

    class Meta:
        db_table = "hum_grupo"