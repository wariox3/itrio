from django.db import models
from general.models.contacto import GenContacto
from general.models.ciudad import GenCiudad
from transporte.models.empaque import TteEmpaque
from transporte.models.operacion import TteOperacion
from transporte.models.producto import TteProducto
from transporte.models.servicio import TteServicio

class TteNegocio(models.Model):
    fecha = models.DateField()
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)  
    nombre = models.CharField(max_length=100, null=True)  
    unidades = models.FloatField(default=0)
    peso = models.FloatField(default=0)
    volumen = models.FloatField(default=0)    
    declara = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    pago = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    flete = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    manejo = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    destinatario_nombre = models.CharField(max_length=150, null=True)
    destinatario_direccion = models.CharField(max_length=150, null=True)
    destinatario_telefono = models.CharField(max_length=50, null=True)
    destinatario_correo = models.CharField(max_length=255, null=True)
    publicar = models.BooleanField(default = False)
    estado_aprobado = models.BooleanField(default = False)
    comentario = models.CharField(max_length=500, null=True)    
    contacto = models.ForeignKey(GenContacto, on_delete=models.PROTECT, related_name='negocios_contacto_rel')
    ciudad_origen = models.ForeignKey(GenCiudad, on_delete=models.PROTECT, related_name='negocios_ciudad_origen_rel')
    ciudad_destino = models.ForeignKey(GenCiudad, on_delete=models.PROTECT, related_name='negocios_ciudad_destino_rel')
    servicio = models.ForeignKey(TteServicio, on_delete=models.PROTECT, related_name='negocios_servicio_rel')
    producto = models.ForeignKey(TteProducto, on_delete=models.PROTECT, related_name='negocios_producto_rel')
    empaque = models.ForeignKey(TteEmpaque, on_delete=models.PROTECT, related_name='negocios_empaque_rel')
    operacion = models.ForeignKey(TteOperacion, on_delete=models.PROTECT, related_name='negocios_operacion_ingreso_rel')
    
    class Meta:
        db_table = "tte_negocio"
        ordering = ["-id"]