from rest_framework import viewsets, permissions
from inquilino.models import Plan
from inquilino.serializers.plan import PlanSerializador

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializador    
    permission_classes = [permissions.IsAuthenticated]    