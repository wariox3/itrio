from django.db import models
from general.models.empresa import GenEmpresa
from general.models.sede import GenSede
from seguridad.models import User

class GenConfiguracionUsuario(models.Model):      
    sede = models.ForeignKey(GenSede, null=True, on_delete=models.PROTECT,related_name='configuraciones_usuarios_sede_rel')
    empresa = models.ForeignKey(GenEmpresa, on_delete=models.PROTECT, default=1)    
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    class Meta:
        db_table = "gen_configuracion_usuario"