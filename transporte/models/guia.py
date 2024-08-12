from django.db import models

class TteGuia(models.Model):
    fecha = models.DateField()
    fechaRecogida = models.DateTimeField(null=True)
    fechaIngreso = models.DateTimeField(null=True)
    fechaDespacho = models.DateTimeField(null=True)
    fechaEntrega = models.DateTimeField(null=True)
    fechaSoporte = models.DateTimeField(null=True)
    documento = models.CharField(max_length=30, null=True)
    destinatario = models.CharField(max_length=150, null=True)
    destinatarioDireccion = models.CharField(max_length=150, null=True)
    destinatarioTelefono = models.CharField(max_length=50, null=True)
    destinatarioCorreo = models.CharField(max_length=255, null=True)
    peso = models.FloatField(default=0)
    volumen = models.FloatField(default=0)
    
    class Meta:
        db_table = "tte_guia"