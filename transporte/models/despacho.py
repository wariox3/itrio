from django.db import models
from general.models.contacto import GenContacto
from general.models.ciudad import GenCiudad
from transporte.models.operacion import TteOperacion
from transporte.models.vehiculo import TteVehiculo
from transporte.models.conductor import TteConductor
from transporte.models.ruta import TteRuta
from transporte.models.despacho_tipo import TteDespachoTipo

class TteDespacho(models.Model):
    fecha_registro = models.DateTimeField(auto_now_add=True)    
    fecha = models.DateField()
    numero = models.IntegerField(null=True)
    numero_rndc = models.IntegerField(null=True)    
    fecha_salida = models.DateTimeField(null=True)
    fecha_llegada = models.DateTimeField(null=True)    
    fecha_entrega = models.DateTimeField(null=True)
    fecha_soporte = models.DateTimeField(null=True)
    pago = models.DecimalField(max_digits=20, decimal_places=6, default=0)    
    precinto = models.CharField(max_length=30, null=True)
    guias = models.FloatField(default=0)
    unidades = models.FloatField(default=0)
    peso = models.FloatField(default=0)
    volumen = models.FloatField(default=0)
    declara = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    flete = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    manejo = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    recaudo = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cobro_entrega = models.DecimalField(max_digits=20, decimal_places=6, default=0) 
    comentario = models.CharField(max_length=500, null=True)                 
    estado_rndc = models.BooleanField(default = False)
    estado_entregado = models.BooleanField(default = False)
    estado_soporte = models.BooleanField(default = False)
    despacho_tipo = models.ForeignKey(TteDespachoTipo, on_delete=models.PROTECT, related_name='despachos_despacho_tipo_rel')    
    operacion = models.ForeignKey(TteOperacion, on_delete=models.PROTECT, related_name='despachos_operacion_rel')
    contacto = models.ForeignKey(GenContacto, on_delete=models.PROTECT, related_name='despachos_contacto_rel')
    ciudad_origen = models.ForeignKey(GenCiudad, on_delete=models.PROTECT, related_name='despachos_ciudad_origen_rel')
    ciudad_destino = models.ForeignKey(GenCiudad, on_delete=models.PROTECT, related_name='despachos_ciudad_destino_rel')
    vehiculo = models.ForeignKey(TteVehiculo, on_delete=models.PROTECT, related_name='despachos_vehiculo_rel')
    remolque = models.ForeignKey(TteVehiculo, on_delete=models.PROTECT, related_name='despachos_remolque_rel')
    ruta = models.ForeignKey(TteRuta, on_delete=models.PROTECT, related_name='despachos_ruta_rel')

    class Meta:
        db_table = "tte_despacho"
        ordering = ["-id"]