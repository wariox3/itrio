from django.db import models

class TteOperacion(models.Model):
    nombre = models.CharField(max_length=50)    
    
    class Meta:
        db_table = "tte_operacion"