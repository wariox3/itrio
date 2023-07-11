from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

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
        db_table = "inq_plan"

class Empresa(TenantMixin):
    schema_name = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200, null=True)
    fecha = models.DateField(auto_now_add=True)
    imagen = models.TextField(null=True)
    usuario_id = models.IntegerField(null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)   
    usuarios = models.IntegerField(default=1) 
    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
    auto_drop_schema = True

    def __str__(self):
        return self.schema_name
    
    class Meta:
        db_table = "inq_empresa"

class Dominio(DomainMixin):
    pass

    class Meta:
        db_table = "inq_dominio"