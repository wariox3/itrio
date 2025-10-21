from django.db import models
from contabilidad.models.conciliacion import ConConciliacion


class ConConciliacionSoporte(models.Model):        
    fecha = models.DateField()
    debito = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    credito = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    detalle = models.CharField(max_length=150, null=True)
    estado_conciliado = models.BooleanField(default = False)    
    conciliacion = models.ForeignKey(ConConciliacion, null=True, on_delete=models.PROTECT, related_name='conciliaciones_soportes_conciliacion_rel')

    class Meta:
        db_table = "con_conciliacion_soporte"
        ordering = ["-id"]