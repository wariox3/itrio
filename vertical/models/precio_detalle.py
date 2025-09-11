from django.db import models
from vertical.models.ciudad import VerCiudad

class VerPrecioDetalle(models.Model):             
    empresa = models.CharField(max_length=200, null=True)
    contenedor_id = models.IntegerField(null=True)
    schema_name = models.CharField(max_length=100, null=True)
    tonelada = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    tonelada_pago = models.DecimalField(max_digits=20, decimal_places=6, default=0)        
    ciudad_origen = models.ForeignKey(VerCiudad, on_delete=models.PROTECT, related_name='precios_detalle_ciudad_origen_rel')
    ciudad_destino = models.ForeignKey(VerCiudad, on_delete=models.PROTECT, related_name='precios_detalles_ciudad_destino_rel')    

    class Meta:
        db_table = "ver_precio_detalle"
        ordering = ["-id"]