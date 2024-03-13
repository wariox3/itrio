from django.db import models
from general.models.identificacion import Identificacion
from general.models.ciudad import Ciudad
from general.models.tipo_persona import TipoPersona
from general.models.regimen import Regimen
from general.models.asesor import Asesor
from general.models.precio import Precio
from general.models.plazo_pago import PlazoPago

class Contacto(models.Model):        
    numero_identificacion = models.CharField(max_length=20, verbose_name='NIT')
    digito_verificacion = models.CharField(max_length=1, null=True, verbose_name='DV')
    nombre_corto = models.CharField(max_length=200, verbose_name='Nombre')
    nombre1 = models.CharField(max_length=50, null=True, verbose_name='Nombre1')
    nombre2 = models.CharField(max_length=50, null=True, verbose_name='Nombre2')
    apellido1 = models.CharField(max_length=50, null=True, verbose_name='Apellido1')
    apellido2 = models.CharField(max_length=50, null=True, verbose_name='Apellido2')
    direccion = models.CharField(max_length=50, verbose_name='Direccion')
    barrio = models.CharField(max_length=200, null=True, verbose_name='Barrio')
    codigo_ciuu = models.CharField(max_length=200, null=True, verbose_name='CIUU')
    codigo_postal = models.CharField(max_length=20, null=True, verbose_name='C_Postal')
    telefono = models.CharField(max_length=50, verbose_name='Telefono')
    celular = models.CharField(max_length=50, verbose_name='Celular')
    correo = models.EmailField(max_length = 255, verbose_name='Correo')
    #Relaciones    
    identificacion = models.ForeignKey(Identificacion, on_delete=models.CASCADE)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.CASCADE)   
    regimen = models.ForeignKey(Regimen, on_delete=models.CASCADE)
    asesor = models.ForeignKey(Asesor, null=True, on_delete=models.CASCADE)
    precio = models.ForeignKey(Precio, null=True, on_delete=models.CASCADE)
    plazo_pago = models.ForeignKey(PlazoPago, null=True, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "gen_contacto"