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
from shapely.geometry import Point, Polygon

def is_point_in_polygon(polygon_coords, point_coords):
    polygon = Polygon(polygon_coords)
    point = Point(point_coords)
    return polygon.contains(point)

class RutFranjaViewSet(viewsets.ModelViewSet):
    queryset = RutFranja.objects.all()
    serializer_class = RutFranjaSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'ubicar',)
    def ubicar(self, request):             
        raw = request.data
        latitud = raw.get('latitud')
        longitud = raw.get('longitud')           

        if latitud and longitud:
            franja = RutFranja.objects.get(pk=1)
            coordenadas = [(coord['longitud'], coord['latitud']) for coord in franja.coordenadas]
            poligono = Polygon(coordenadas)                
            punto = Point(latitud,longitud)            
            if poligono.contains(punto):
                return Response({'franja': 'SI'}, status=status.HTTP_200_OK)
            else:
                return Response({'franja': 'NO'}, status=status.HTTP_200_OK)                                
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
