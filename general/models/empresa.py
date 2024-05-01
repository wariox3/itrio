from django.db import models
from general.models.identificacion import Identificacion
from general.models.ciudad import Ciudad
from general.models.tipo_persona import TipoPersona
from general.models.regimen import Regimen

class Empresa(models.Model):   
    id = models.BigIntegerField(primary_key=True)     
    numero_identificacion = models.CharField(max_length=20)
    digito_verificacion = models.CharField(max_length=1)
    nombre_corto = models.CharField(max_length=200)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, null=True)
    correo = models.EmailField(max_length = 255)
    imagen = models.TextField(null=True)
    contenedor_id = models.IntegerField()     
    rededoc_id = models.IntegerField(null=True)    
    subdominio = models.CharField(max_length=100, default='demo') 
    identificacion = models.ForeignKey(Identificacion, on_delete=models.PROTECT)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.PROTECT)   
    regimen = models.ForeignKey(Regimen, on_delete=models.PROTECT)
    class Meta:
        db_table = "gen_empresa"