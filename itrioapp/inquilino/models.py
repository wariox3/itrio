from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Cliente(TenantMixin):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

class Dominio(DomainMixin):
    pass
