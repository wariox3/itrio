from django.db import models

class GenRespuestaElectronica(models.Model):        
    codigo_estatus = models.CharField(max_length=10, null=True)
    proceso_dian = models.CharField(max_length=1, null=True)
    mensaje_error = models.TextField(null=True)
    razon_error = models.TextField(null=True)
    codigo_modelo = models.IntegerField()
    fecha = models.DateField()

    class Meta:
        db_table = "gen_respuesta_electronica"