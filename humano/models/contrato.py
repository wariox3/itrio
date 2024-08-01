from django.db import models
from general.models.contacto import GenContacto
from humano.models.contrato_tipo import HumContratoTipo
from humano.models.grupo import HumGrupo

class HumContrato(models.Model):        
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    estado_terminado = models.BooleanField(default = False)
    contrato_tipo = models.ForeignKey(HumContratoTipo, on_delete=models.PROTECT, related_name='contratos_contrato_tipo_rel')
    contacto = models.ForeignKey(GenContacto, on_delete=models.PROTECT, related_name='contratos_contacto_rel')
    grupo = models.ForeignKey(HumGrupo, on_delete=models.PROTECT, related_name='contratos_grupo_rel')

    class Meta:
        db_table = "hum_contrato"   