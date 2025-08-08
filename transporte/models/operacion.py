from django.db import models
from general.models.ciudad import GenCiudad

class TteOperacion(models.Model):
    nombre = models.CharField(max_length=50)    
    ciudad = models.ForeignKey(GenCiudad, on_delete=models.PROTECT, related_name='operaciones_ciudad_rel')
    
    class Meta:
        db_table = "tte_operacion"
        ordering = ["-id"]