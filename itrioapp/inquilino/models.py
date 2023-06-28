from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Empresa(TenantMixin):
    schema_name = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200, null=True)
    fecha = models.DateField(auto_now_add=True)
    imagen = models.TextField(null=True)
    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return self.schema_name

class Dominio(DomainMixin):
    pass
