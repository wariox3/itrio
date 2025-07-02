from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from crm.models.presupuesto import CrmPresupuesto
from crm.serializers.presupuesto import CrmPresupuestoSerializador

class PresupuestoViewSet(viewsets.ModelViewSet):
    queryset = CrmPresupuesto.objects.all()
    serializer_class = CrmPresupuestoSerializador
    permission_classes = [permissions.IsAuthenticated]                         