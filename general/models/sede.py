from django.db import models

class Sede(models.Model):        
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = "gen_sede"