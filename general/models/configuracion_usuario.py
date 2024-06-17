from django.db import models
from general.models.empresa import Empresa
from general.models.sede import Sede
from seguridad.models import User

class ConfiguracionUsuario(models.Model):      
    sede = models.ForeignKey(Sede, null=True, on_delete=models.PROTECT,related_name='configuraciones_usuarios_sede_rel')
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, default=1)    
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    class Meta:
        db_table = "gen_configuracion_usuario"