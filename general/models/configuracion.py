from django.db import models
from general.models.empresa import Empresa

class Configuracion(models.Model):   
    id = models.BigIntegerField(primary_key=True)     
    formato_factura = models.CharField(max_length=2, default='F')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, default=1)
    class Meta:
        db_table = "gen_configuracion"