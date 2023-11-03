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
    telefono = models.CharField(max_length=50)
    correo = models.EmailField(max_length = 255)
    imagen = models.TextField(null=True)
    contenedor_id = models.IntegerField()     
    suscriptor = models.CharField(max_length=200,null=True)
    identificacion = models.ForeignKey(Identificacion, on_delete=models.CASCADE)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.CASCADE)   
    regimen = models.ForeignKey(Regimen, on_delete=models.CASCADE)
    class Meta:
        db_table = "gen_empresa"