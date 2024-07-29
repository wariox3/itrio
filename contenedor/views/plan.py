from rest_framework import viewsets, permissions
from contenedor.models import CtnPlan
from contenedor.serializers.plan import CtnPlanSerializador

class PlanViewSet(viewsets.ModelViewSet):
    queryset = CtnPlan.objects.all()
    serializer_class = CtnPlanSerializador    
    permission_classes = [permissions.IsAuthenticated]    