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
                cantidad = 0
                #kml_file = "/home/desarrollo/Escritorio/franjas.kml"
                #tree = ET.parse(kml_file)
                archivo_decodificado = base64.b64decode(archivoB64)
                archivo_contenido = ContentFile(archivo_decodificado, "franjas.kml")
                tree = ET.parse(archivo_contenido)
                root = tree.getroot()
                namespace = {"kml": "http://www.opengis.net/kml/2.2"}
                
                # Buscar el style del color
                def get_style_color(style_id):                
                    style = root.find(f".//kml:Style[@id='{style_id}']", namespace)
                    if style is not None:
                        poly_style = style.find(".//kml:PolyStyle/kml:color", namespace)
                        line_style = style.find(".//kml:LineStyle/kml:color", namespace)
                        if poly_style is not None:
                            return poly_style.text
                        elif line_style is not None:
                            return line_style.text
                    
                    style_map = root.find(f".//kml:StyleMap[@id='{style_id}']", namespace)
                    if style_map is not None:
                        normal_pair = style_map.find(".//kml:Pair[kml:key='normal']/kml:styleUrl", namespace)
                        if normal_pair is not None:
                            return get_style_color(normal_pair.text.replace("#", ""))                
                    return None

                for placemark in root.findall(".//kml:Placemark", namespace):
                    nombre = placemark.find("kml:name", namespace)
                    poligono = placemark.find(".//kml:Polygon", namespace)    
                    style_url = placemark.find("kml:styleUrl", namespace)
                    color = None
                    
                    if style_url is not None:
                        style_id = style_url.text.replace("#", "")
                        color = get_style_color(style_id)            
                        #print(f"Style ID: {style_id}, Color encontrado: {color}")

                    if nombre is not None and poligono is not None:
                        nombre = nombre.text
                        coordinates = poligono.find(".//kml:coordinates", namespace).text.strip()                

                        coord_list = []
                        for coord in coordinates.split():
                            lon, lat, *_ = coord.split(",")
                            coord_list.append({'lat': float(lat), 'lng': float(lon)})

                        data = {
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
