from django.db import models
from ruteo.models.rut_despacho import RutDespacho

class RutVisita(models.Model):
    guia = models.IntegerField(null=True)
    fecha = models.DateField(null=True)    
    documento = models.CharField(max_length=30, null=True)
    destinatario = models.CharField(max_length=150, null=True)
    destinatario_direccion = models.CharField(max_length=150, null=True)
    destinatario_telefono = models.CharField(max_length=50, null=True)
    destinatario_correo = models.CharField(max_length=255, null=True)
    peso = models.FloatField(default=0)
    volumen = models.FloatField(default=0)
    ciudad = models.CharField(max_length=50, null=True)
    estado = models.CharField(max_length=50, null=True)
    pais = models.CharField(max_length=50, null=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    decodificado = models.BooleanField(default = False)
    decodificado_error = models.BooleanField(default = False)
    estado_despacho = models.BooleanField(default = False)
    orden = models.IntegerField(default=0)
    distancia_proxima = models.DecimalField(max_digits=9, decimal_places=6, null=True, default=0)
    despacho = models.ForeignKey(RutDespacho, null=True, on_delete=models.PROTECT, related_name='visitas_despacho_rel')

    class Meta:
        db_table = "rut_visita"