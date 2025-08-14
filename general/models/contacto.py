from django.db import models
from general.models.identificacion import GenIdentificacion
from general.models.ciudad import GenCiudad
from general.models.tipo_persona import GenTipoPersona
from general.models.regimen import GenRegimen
from general.models.asesor import GenAsesor
from general.models.precio import GenPrecio
from general.models.plazo_pago import GenPlazoPago
from general.models.banco import GenBanco
from general.models.cuenta_banco_clase import GenCuentaBancoClase

class GenContacto(models.Model):        
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
    correo_facturacion_electronica = models.CharField(max_length = 255, null=True)
    cliente = models.BooleanField(default = False) 
    proveedor = models.BooleanField(default = False)
    empleado = models.BooleanField(default = False)
    conductor = models.BooleanField(default = False)
    numero_cuenta = models.CharField(max_length=50, null=True)
    numero_licencia = models.CharField(max_length=50, null=True)
    categoria_licencia = models.CharField(max_length=2, null=True)
    fecha_vence_licencia = models.DateField(null=True)
    identificacion = models.ForeignKey(GenIdentificacion, on_delete=models.PROTECT)
    ciudad = models.ForeignKey(GenCiudad, on_delete=models.PROTECT)
    tipo_persona = models.ForeignKey(GenTipoPersona, on_delete=models.PROTECT)   
    regimen = models.ForeignKey(GenRegimen, on_delete=models.PROTECT)
    asesor = models.ForeignKey(GenAsesor, null=True, on_delete=models.PROTECT)
    precio = models.ForeignKey(GenPrecio, null=True, on_delete=models.PROTECT)
    plazo_pago = models.ForeignKey(GenPlazoPago, null=True, on_delete=models.PROTECT, related_name='contactos_plazo_pago')
    plazo_pago_proveedor = models.ForeignKey(GenPlazoPago, null=True, on_delete=models.PROTECT, related_name='contactos_plazo_pago_proveedor')
    banco = models.ForeignKey(GenBanco, null=True, on_delete=models.PROTECT)
    cuenta_banco_clase = models.ForeignKey(GenCuentaBancoClase, null=True, on_delete=models.PROTECT)
    
    class Meta:
        db_table = "gen_contacto"
        ordering = ["-id"]