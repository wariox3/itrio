from django.db import models
from general.models.estado import Estado

class FormaPago(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50) 
    
    class Meta:
        db_table = "gen_forma_pago"