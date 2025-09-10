from django.db import models
from vertical.models.ciudad import VerCiudad
from vertical.models.vehiculo import VerVehiculo
from vertical.models.conductor import VerConductor
from vertical.models.servicio import VerServicio
from vertical.models.producto import VerProducto
from vertical.models.empaque import VerEmpaque

from seguridad.models import User

class VerViaje(models.Model):            
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    numero_identificacion = models.CharField(max_length=20, null=True)
    cliente = models.CharField(max_length=200, null=True)
    unidades = models.FloatField(default=0)    
    flete = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    pago = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    peso = models.FloatField(default=0)
    volumen = models.FloatField(default=0)
    puntos_entrega = models.IntegerField(default=0)
    negocio_id = models.IntegerField(null=True)
    contenedor_id = models.IntegerField(null=True)
    schema_name = models.CharField(max_length=100, null=True)
    solicitud_cliente = models.BooleanField(default=False)
    solicitud_transporte = models.BooleanField(default=False)
    estado_aceptado = models.BooleanField(default=False)
    estado_cancelado = models.BooleanField(default=False)    
    propuestas = models.IntegerField(default=0)
    comentario = models.CharField(max_length=500, null=True)
    ciudad_origen = models.ForeignKey(VerCiudad, on_delete=models.PROTECT, related_name='viajes_ciudad_origen_rel')
    ciudad_destino = models.ForeignKey(VerCiudad, on_delete=models.PROTECT, related_name='viajes_ciudad_destino_rel')    
    vehiculo = models.ForeignKey(VerVehiculo, null=True, on_delete=models.PROTECT, related_name='viajes_vehiculo_rel')
    conductor = models.ForeignKey(VerConductor, null=True, on_delete=models.PROTECT, related_name='viajes_conductor_rel')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='viajes_usuario_rel')
    servicio = models.ForeignKey(VerServicio, null=True, on_delete=models.PROTECT, related_name='viajes_servicio_rel')
    producto = models.ForeignKey(VerProducto, null=True, on_delete=models.PROTECT, related_name='viajes_producto_rel')
    empaque = models.ForeignKey(VerEmpaque, null=True, on_delete=models.PROTECT, related_name='viajes_empaque_rel')    

    class Meta:
        db_table = "ver_viaje"
        ordering = ["-id"]