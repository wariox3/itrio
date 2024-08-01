from django.db import models

class RutFranja(models.Model):
    nombre = models.CharField(max_length=255)
    coordenadas = models.JSONField()
    '''coordenadas = [
        {'lat': 0, 'lng': 0},
        {'lat': 1, 'lng': 1},
        {'lat': 1, 'lng': 0},
        {'lat': 0, 'lng': 0}
    ]'''

    class Meta:
        db_table = "rut_franja"