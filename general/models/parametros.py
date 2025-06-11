from django.db import models

class GenParametros(models.Model):   
    id = models.BigIntegerField(primary_key=True)                 
    uvt = models.DecimalField(max_digits=20, decimal_places=6, default=47065)
    factor = models.DecimalField(max_digits=6, decimal_places=3, default=7.666)
    salario_minimo = models.DecimalField(max_digits=20, decimal_places=6, default=1300000)
    auxilio_transporte = models.DecimalField(max_digits=20, decimal_places=6, default=162000)    
    class Meta:
        db_table = "gen_parametros"
        ordering = ["-id"]