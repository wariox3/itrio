from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.color import VerColor
from vertical.serializers.color import VerColorSerializador

class ColorViewSet(viewsets.ModelViewSet):
    queryset = VerColor.objects.all()
    serializer_class = VerColorSerializador
    permission_classes = [permissions.IsAuthenticated]