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
import xml.etree.ElementTree as ET
from django.core.files.base import ContentFile

def is_point_in_polygon(polygon_coords, point_coords):
    polygon = Polygon(polygon_coords)
    point = Point(point_coords)
    return polygon.contains(point)

class RutFranjaViewSet(viewsets.ModelViewSet):
    queryset = RutFranja.objects.all()
    serializer_class = RutFranjaSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'importar',)
    def importar(self, request):             
        raw = request.data
        archivoB64 = raw.get('base64')
        if archivoB64:
            try:
                franjas = RutFranja.objects.all().delete()
                cantidad = 0
                archivo_decodificado = base64.b64decode(archivoB64)
                archivo_contenido = ContentFile(archivo_decodificado, "franjas.kml")
                tree = ET.parse(archivo_contenido)
                root = tree.getroot()
                namespace = {"kml": "http://www.opengis.net/kml/2.2"}                                           
                for placemark in root.findall(".//kml:Placemark", namespace):
                    nombre = placemark.find("kml:name", namespace)
                    poligono = placemark.find(".//kml:Polygon", namespace)    
                    style_url = placemark.find("kml:styleUrl", namespace)
                    color = None

                    if style_url is not None:
                        style_id = style_url.text.replace("#", "") + "-normal"                         
                        style = root.find(f".//kml:Style[@id='{style_id}']", namespace)                        
                        if style is not None:                            
                            poly_style = style.find(".//kml:PolyStyle/kml:color", namespace)
                            if poly_style is not None:
                                color = poly_style.text[2:]                        

                    if nombre is not None and poligono is not None:
                        nombre = nombre.text
                        coordinates = poligono.find(".//kml:coordinates", namespace).text.strip()                

                        coord_list = []
                        for coord in coordinates.split():
                            lon, lat, *_ = coord.split(",")
                            coord_list.append({'lat': float(lat), 'lng': float(lon)})

                        data = {
                            "codigo": nombre,
                            "nombre": nombre,
                            "coordenadas": coord_list,
                            "color": color
                        }                        
                        franja_serializador = RutFranjaSerializador(data=data)
                        if franja_serializador.is_valid():
                            franja_serializador.save()
                            cantidad += 1
                        else:
                            return Response({'validaciones':franja_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'mensaje': f'Se importaron {cantidad} de franjas desde el archivo kml'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'mensaje':'Ocurrio un error inesperado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)            
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)        
