from django.db import models
from general.models.contacto import GenContacto
from general.models.ciudad import GenCiudad
from transporte.models.color import TteColor
from transporte.models.marca import TteMarca
from transporte.models.linea import TteLinea
from transporte.models.combustible import TteCombustible
from transporte.models.carroceria import TteCarroceria
from transporte.models.vehiculo_configuracion import TteVehiculoConfiguracion

class TteVehiculo(models.Model):    
    fecha_registro = models.DateTimeField(auto_now_add=True)        
    placa = models.CharField(max_length=6)
    modelo = models.IntegerField()
    modelo_repotenciado = models.IntegerField(null=True)
    motor = models.CharField(max_length=50, null=True)
    chasis = models.CharField(max_length=50, null=True)
    ejes = models.IntegerField()
    peso_vacio = models.IntegerField()    
    capacidad = models.IntegerField()
    celular = models.CharField(max_length=50, null=True)
    poliza = models.CharField(max_length=30, null=True)
    vence_poliza = models.DateField()
    tecnicomecanica = models.CharField(max_length=30, null=True)
    vence_tecnicomecanica = models.DateField()
    propio = models.BooleanField(default = False)
    remolque = models.BooleanField(default = False)
    estado_inactivo = models.BooleanField(default = False)
    estado_revisado = models.BooleanField(default = False)
    comentario = models.CharField(max_length=500, null=True)
    poseedor = models.ForeignKey(GenContacto, on_delete=models.PROTECT, related_name='vehiculos_poseedor_rel')
    propietario = models.ForeignKey(GenContacto, on_delete=models.PROTECT, related_name='vehiculos_propietario_rel')
    aseguradora = models.ForeignKey(GenContacto, on_delete=models.PROTECT, related_name='vehiculos_aeguradora_rel')
    color = models.ForeignKey(TteColor, on_delete=models.PROTECT, related_name='vehiculos_color_rel')
    marca = models.ForeignKey(TteMarca, on_delete=models.PROTECT, related_name='vehiculos_marca_rel')
    linea = models.ForeignKey(TteLinea, on_delete=models.PROTECT, related_name='vehiculos_linea_rel')
    combustible = models.ForeignKey(TteCombustible, on_delete=models.PROTECT, related_name='vehiculos_combustible_rel')
    carroceria = models.ForeignKey(TteCarroceria, on_delete=models.PROTECT, related_name='vehiculos_carroceria_rel')
    configuracion = models.ForeignKey(TteVehiculoConfiguracion, on_delete=models.PROTECT, related_name='vehiculos_vehiculo_configuracion_rel')    

    class Meta:
        db_table = "tte_vehiculo"
        ordering = ["-id"]