from django.db import models
from general.models.identificacion import GenIdentificacion
from general.models.ciudad import GenCiudad
from general.models.tipo_persona import GenTipoPersona
from general.models.regimen import GenRegimen

class GenEmpresa(models.Model):   
    id = models.BigIntegerField(primary_key=True)     
    numero_identificacion = models.CharField(max_length=20, null=True)
    digito_verificacion = models.CharField(max_length=1, null=True)
    nombre_corto = models.CharField(max_length=200)
    direccion = models.CharField(max_length=50, null=True)
    telefono = models.CharField(max_length=50, null=True)
    correo = models.EmailField(max_length = 255)
    imagen = models.TextField(null=True)
    contenedor_id = models.IntegerField()     
    rededoc_id = models.IntegerField(null=True)    
    subdominio = models.CharField(max_length=100, default='demo') 
    asistente_electronico = models.BooleanField(default = False)
    asistente_predeterminado = models.BooleanField(default = False)
    identificacion = models.ForeignKey(GenIdentificacion, null=True, on_delete=models.PROTECT)
    ciudad = models.ForeignKey(GenCiudad, null=True, on_delete=models.PROTECT)
    tipo_persona = models.ForeignKey(GenTipoPersona, null=True, on_delete=models.PROTECT)   
    regimen = models.ForeignKey(GenRegimen, null=True, on_delete=models.PROTECT)
    class Meta:
        db_table = "gen_empresa"
        ordering = ["-id"]