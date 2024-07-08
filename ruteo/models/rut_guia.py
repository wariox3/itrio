from django.db import models

class RutGuia(models.Model):
    guia = models.IntegerField(null=True)
    fecha = models.DateField(null=True)    
    documento = models.CharField(max_length=30, null=True)
    destinatario = models.CharField(max_length=150, null=True)
    destinatario_direccion = models.CharField(max_length=150, null=True)
    destinatario_telefono = models.CharField(max_length=50, null=True)
    destinatario_correo = models.CharField(max_length=255, null=True)
    peso = models.FloatField(default=0)
    volumen = models.FloatField(default=0)
    
    class Meta:
        db_table = "rut_guia"