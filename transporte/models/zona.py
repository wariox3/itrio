from django.db import models

class TteZona(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = "tte_zona"