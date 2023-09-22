from rest_framework import viewsets, permissions
from contenedor.models import Plan
from contenedor.serializers.plan import PlanSerializador

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializador    
    permission_classes = [permissions.IsAuthenticated]    