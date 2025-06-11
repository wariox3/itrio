from django.db import models

class TteRuta(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = "tte_ruta"
        ordering = ["-id"]