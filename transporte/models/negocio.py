from django.db import models
from general.models.contacto import GenContacto
from general.models.ciudad import GenCiudad

class TteNegocio(models.Model):
    fecha = models.DateField()
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)    
    unidades = models.FloatField(default=0)
    peso = models.FloatField(default=0)
    volumen = models.FloatField(default=0)    
    declara = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    pago = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    flete = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    manejo = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    comentario = models.CharField(max_length=500, null=True)
    contacto = models.ForeignKey(GenContacto, on_delete=models.PROTECT, related_name='negocios_contacto_rel')
    ciudad_origen = models.ForeignKey(GenCiudad, on_delete=models.PROTECT, related_name='negocios_ciudad_origen_rel')
    ciudad_destino = models.ForeignKey(GenCiudad, on_delete=models.PROTECT, related_name='negocios_ciudad_destino_rel')
    
    class Meta:
        db_table = "tte_negocio"
        ordering = ["-id"]