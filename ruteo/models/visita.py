from django.db import models
from ruteo.models.despacho import RutDespacho
from ruteo.models.franja import RutFranja
from general.models.ciudad import GenCiudad

class RutVisita(models.Model):
    guia = models.IntegerField(null=True)
    fecha = models.DateTimeField(null=True)    
    documento = models.CharField(max_length=30, null=True)
    destinatario = models.CharField(max_length=150, default='Destinatario')
    destinatario_direccion = models.CharField(max_length=150, default='')
    destinatario_direccion_formato = models.CharField(max_length=150, null=True, default='')
    destinatario_telefono = models.CharField(max_length=50, null=True)
    destinatario_correo = models.CharField(max_length=255, null=True)
    peso = models.FloatField(default=0)
    volumen = models.FloatField(default=0)
    latitud = models.DecimalField(max_digits=20, decimal_places=12, null=True)
    longitud = models.DecimalField(max_digits=20, decimal_places=12, null=True)
    estado_decodificado = models.BooleanField(null=True, default = None)
    estado_franja = models.BooleanField(null=True, default=None)
    estado_despacho = models.BooleanField(default = False)
    orden = models.IntegerField(default=0)
    distancia_proxima = models.DecimalField(max_digits=9, decimal_places=6, null=True, default=0)
    despacho = models.ForeignKey(RutDespacho, null=True, on_delete=models.PROTECT, related_name='visitas_despacho_rel')
    franja = models.ForeignKey(RutFranja, null=True, on_delete=models.PROTECT, related_name='visitas_franja_rel')
    ciudad = models.ForeignKey(GenCiudad, null=True, on_delete=models.PROTECT, default=1, related_name='visitas_ciudad_rel')

    class Meta:
        db_table = "rut_visita"