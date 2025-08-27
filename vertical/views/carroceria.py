from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.carroceria import VerCarroceria
from vertical.serializers.carroceria import VerCarroceriaSerializador

class CarroceriaViewSet(viewsets.ModelViewSet):
    queryset = VerCarroceria.objects.all()
    serializer_class = VerCarroceriaSerializador
    permission_classes = [permissions.IsAuthenticated]