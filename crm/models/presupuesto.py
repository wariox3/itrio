from django.db import models
from general.models.contacto import GenContacto

class CrmPresupuesto(models.Model):        
    fecha = models.DateField()
    vence = models.DateField()
    contacto = models.ForeignKey(GenContacto, on_delete=models.PROTECT, related_name='presupuestos_contacto_rel')
    
    class Meta:
        db_table = "crm_presupuesto"
        ordering = ["-id"]