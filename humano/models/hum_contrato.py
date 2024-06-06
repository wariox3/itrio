from django.db import models
from general.models.contacto import Contacto

class HumContrato(models.Model):        
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    #contacto = models.ForeignKey(Contacto, on_delete=models.PROTECT, related_name='contratos_contacto_rel')

    class Meta:
        db_table = "hum_contrato"