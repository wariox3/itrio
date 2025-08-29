from django.db import models
from vertical.models.marca import VerMarca
from vertical.models.linea import VerLinea
from vertical.models.color import VerColor
from vertical.models.combustible import VerCombustible
from vertical.models.carroceria import VerCarroceria
from vertical.models.vehiculo_configuracion import VerVehiculoConfiguracion

class VerVehiculo(models.Model):        
    fecha_registro = models.DateTimeField(auto_now_add=True)  
    placa = models.CharField(max_length=6)
    modelo = models.IntegerField()
    modelo_repotenciado = models.IntegerField(null=True)
    motor = models.CharField(max_length=50, null=True)
    chasis = models.CharField(max_length=50, null=True)
    ejes = models.IntegerField()
    peso_vacio = models.IntegerField()    
    capacidad = models.IntegerField()
    poliza = models.CharField(max_length=30, null=True)
    vence_poliza = models.DateField()
    tecnicomecanica = models.CharField(max_length=30, null=True)
    vence_tecnicomecanica = models.DateField()
    propio = models.BooleanField(default = False)
    remolque = models.BooleanField(default = False)
    verificado = models.BooleanField(default = False)
    marca = models.ForeignKey(VerMarca, on_delete=models.PROTECT, related_name='vehiculos_marca_rel')
    linea = models.ForeignKey(VerLinea, on_delete=models.PROTECT, related_name='vehiculos_linea_rel')
    color = models.ForeignKey(VerColor, on_delete=models.PROTECT, related_name='vehiculos_color_rel')
    combustible = models.ForeignKey(VerCombustible, on_delete=models.PROTECT, related_name='vehiculos_combustible_rel')
    carroceria = models.ForeignKey(VerCarroceria, on_delete=models.PROTECT, related_name='vehiculos_carroceria_rel')
    configuracion = models.ForeignKey(VerVehiculoConfiguracion, on_delete=models.PROTECT, related_name='vehiculos_vehiculo_configuracion_rel')

    class Meta:
        db_table = "ver_vehiculo"
        ordering = ["-id"]