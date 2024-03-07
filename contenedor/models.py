from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from seguridad.models import User

class ContenedorPais(models.Model):
    id = models.CharField(primary_key=True, max_length=2)
    nombre = models.CharField(max_length=50, null=True)
    codigo = models.CharField(max_length=10, null=True)
    
    class Meta:
        db_table = "cnt_pais"

class ContenedorEstado(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=10, null=True)
    pais = models.ForeignKey(ContenedorPais, on_delete=models.CASCADE)

    class Meta:
        db_table = "cnt_estado"

class ContenedorRegimen(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50) 
    
    class Meta:
        db_table = "cnt_regimen"        

class ContenedorTipoPersona(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50) 
    
    class Meta:
        db_table = "cnt_tipo_persona"    

class ContenedorIdentificacion(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)    
    orden = models.BigIntegerField(default=0)
    codigo = models.CharField(max_length=10, null=True)
    pais = models.ForeignKey(ContenedorPais, on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = "cnt_identificacion"

class Plan(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50, null=True)
    limite_usuarios = models.IntegerField(default=0)
    usuarios_base = models.IntegerField(default=0)
    limite_ingresos = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    precio_usuario_adicional = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    limite_electronicos = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    class Meta:
        db_table = "cnt_plan"

class Contenedor(TenantMixin):
    schema_name = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    imagen = models.TextField(null=True)
    usuario_id = models.IntegerField(null=True)
    usuarios = models.IntegerField(default=1) 
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)         
    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
    auto_drop_schema = True

    def __str__(self):
        return self.schema_name
    
    class Meta:
        db_table = "cnt_contenedor"

class Dominio(DomainMixin):
    pass

    class Meta:
        db_table = "cnt_dominio"

class Consumo(models.Model):
    fecha = models.DateField(null=True)
    contenedor_id = models.IntegerField(null=True)
    contenedor = models.CharField(max_length=200, null=True)    
    usuarios = models.IntegerField(default=0) 
    vr_plan = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    vr_usuario_adicional = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    vr_total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "cnt_consumo"

class Verificacion(models.Model):
    usuario_id = models.IntegerField(null=True)
    contenedor_id = models.IntegerField(null=True)
    token = models.CharField(max_length=50)
    estado_usado = models.BooleanField(default = False)
    vence = models.DateField(null=True)
    accion = models.CharField(max_length=10, default='registro')
    usuario_invitado_username = models.EmailField(max_length = 255, null=True)

    class Meta:
        db_table = "cnt_verificacion" 

class UsuarioContenedor(models.Model):
    rol = models.CharField(max_length=20, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenedor = models.ForeignKey(Contenedor, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('usuario', 'contenedor')
        db_table = "cnt_usuario_contenedor"        

class ContenedorMovimiento(models.Model):
    tipo = models.CharField(max_length=20, null=True)
    fecha = models.DateField(null=True)    
    vr_total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    vr_afectado = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    vr_saldo = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "cnt_movimiento"        