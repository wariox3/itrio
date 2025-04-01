from django.db import models
from ruteo.models.despacho import RutDespacho
from ruteo.models.visita import RutVisita

class RutUbicacion(models.Model):    
    fecha = models.DateTimeField(auto_now_add=True)  
    latitud = models.DecimalField(max_digits=25, decimal_places=15)
    longitud = models.DecimalField(max_digits=25, decimal_places=15)
    despacho = models.ForeignKey(RutDespacho, null=True, on_delete=models.PROTECT, related_name='ubicaciones_despacho_rel')
    visita = models.ForeignKey(RutVisita, null=True, on_delete=models.PROTECT, related_name='ubicaciones_visita_rel')

    class Meta:
        db_table = "rut_ubicacion"