from django.db import models

class VerEntrega(models.Model):        
    
    contenedor_id = models.IntegerField() 
    usuario_id = models.IntegerField()

    class Meta:
        db_table = "ver_entrega"