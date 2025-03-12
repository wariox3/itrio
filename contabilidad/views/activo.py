from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.activo import ConActivo
from contabilidad.serializers.activo import ConActivoSerializador
from django.db.models import ProtectedError
from io import BytesIO
import base64
import openpyxl
import gc
import os

class ActivoViewSet(viewsets.ModelViewSet):
    queryset = ConActivo.objects.all()
    serializer_class = ConActivoSerializador
    permission_classes = [permissions.IsAuthenticated]
           
        
    