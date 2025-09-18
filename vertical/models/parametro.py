from django.db import models

class VerParametro(models.Model):            
    id = models.BigIntegerField(primary_key=True)    
    version_ruteo_android = models.CharField(max_length=50, null=True)    
    version_ruteo_ios = models.CharField(max_length=50, null=True)    

    class Meta:
        db_table = "ver_parametro"
        ordering = ["-id"]