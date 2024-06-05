from django.db import models
from general.models.identificacion import Identificacion
from general.models.ciudad import Ciudad
from general.models.tipo_persona import TipoPersona
from general.models.regimen import Regimen
from general.models.asesor import Asesor
from general.models.precio import Precio
from general.models.plazo_pago import PlazoPago

class Contacto(models.Model):        
    numero_identificacion = models.CharField(max_length=20)
    digito_verificacion = models.CharField(max_length=1, null=True)
    nombre_corto = models.CharField(max_length=200)
    nombre1 = models.CharField(max_length=50, null=True)
    nombre2 = models.CharField(max_length=50, null=True)
    apellido1 = models.CharField(max_length=50, null=True)
    apellido2 = models.CharField(max_length=50, null=True)
    direccion = models.CharField(max_length=100)
    barrio = models.CharField(max_length=200, null=True)
    codigo_ciuu = models.CharField(max_length=200, null=True)
    codigo_postal = models.CharField(max_length=20, null=True)
    telefono = models.CharField(max_length=50)
    celular = models.CharField(max_length=50, null=True)
    correo = models.CharField(max_length = 255)
    cliente = models.BooleanField(default = False) 
    proveedor = models.BooleanField(default = False)
    empleado = models.BooleanField(default = False)
    #Relaciones    
    identificacion = models.ForeignKey(Identificacion, on_delete=models.PROTECT)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.PROTECT)   
    regimen = models.ForeignKey(Regimen, on_delete=models.PROTECT)
    asesor = models.ForeignKey(Asesor, null=True, on_delete=models.PROTECT)
    precio = models.ForeignKey(Precio, null=True, on_delete=models.PROTECT)
    plazo_pago = models.ForeignKey(PlazoPago, null=True, on_delete=models.PROTECT, related_name='contactos_plazo_pago')
    plazo_pago_proveedor = models.ForeignKey(PlazoPago, null=True, on_delete=models.PROTECT, related_name='contactos_plazo_pago_proveedor')
    
    class Meta:
        db_table = "gen_contacto"