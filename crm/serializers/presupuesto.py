from rest_framework import serializers
from crm.models.presupuesto import CrmPresupuesto
from general.models.contacto import GenContacto

class CrmPresupuestoSerializador(serializers.HyperlinkedModelSerializer):           
    contacto = serializers.PrimaryKeyRelatedField(queryset=GenContacto.objects.all())

    class Meta:
        model = CrmPresupuesto
        fields = ['id', 'fecha']         
        