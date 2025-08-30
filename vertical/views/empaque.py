from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.empaque import VerEmpaque
from vertical.serializers.empaque import VerEmpaqueSerializador

class EmpaqueViewSet(viewsets.ModelViewSet):
    queryset = VerEmpaque.objects.all()
    serializer_class = VerEmpaqueSerializador
    permission_classes = [permissions.IsAuthenticated]