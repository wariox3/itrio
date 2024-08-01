from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ruteo.models.franja import RutFranja
from ruteo.serializers.franja import RutFranjaSerializador
import base64
from io import BytesIO
import openpyxl
from datetime import datetime
from decouple import config
import json
from utilidades.zinc import Zinc

class RutFranjaViewSet(viewsets.ModelViewSet):
    queryset = RutFranja.objects.all()
    serializer_class = RutFranjaSerializador
    permission_classes = [permissions.IsAuthenticated]