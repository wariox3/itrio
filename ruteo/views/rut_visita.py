from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ruteo.models.rut_visita import RutVisita
from ruteo.models.rut_despacho import RutDespacho
from ruteo.models.rut_vehiculo import RutVehiculo
from ruteo.serializers.rut_visita import RutVisitaSerializador
import base64
from io import BytesIO
import openpyxl
from datetime import datetime
from django.utils import timezone
from decouple import config
import json
from utilidades.zinc import Zinc
from math import radians, cos, sin, asin, sqrt

def calcular_distancia(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Fórmula de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

def ordenar_ruta(visitas, lat_inicial, lon_inicial):
    visitas_con_distancias = []
    for visita in visitas:
        distancia = calcular_distancia(lat_inicial, lon_inicial, visita.latitud, visita.longitud)
        visita.distancia_proxima = distancia
        visitas_con_distancias.append((visita, distancia))

    visitas_con_distancias.sort(key=lambda x: x[1])
    for index, (visita, _) in enumerate(visitas_con_distancias):
        visita.orden = index + 1
        visita.save()
    return [visita for visita, _ in visitas_con_distancias]        
    #direcciones_ordenadas = [visita for visita, distancia in visitas_con_distancias]    
    #return direcciones_ordenadas

class RutVisitaViewSet(viewsets.ModelViewSet):
    queryset = RutVisita.objects.all()
    serializer_class = RutVisitaSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'importar',)
    def importar(self, request):
        raw = request.data
        archivo_base64 = raw.get('archivo_base64')
        if archivo_base64:
            archivo_data = base64.b64decode(archivo_base64)
            archivo = BytesIO(archivo_data)
            wb = openpyxl.load_workbook(archivo)
            sheet = wb.active    
            for row in sheet.iter_rows(min_row=2, values_only=True):
                fecha_texto = str(row[1])
                fecha = datetime.strptime(fecha_texto, '%Y%m%d').date()
                documento = str(row[2])
                telefono_destinatario = str(row[8])
                data = {
                    'guia': row[0],
                    'fecha':fecha,
                    'documento': documento[:30],
                    'destinatario': row[3],
                    'destinatario_direccion': row[4],
                    'ciudad': row[5],
                    'estado': row[6],
                    'pais': row[7],
                    'destinatario_telefono': telefono_destinatario[:50],
                    'destinatario_correo': row[9],
                    'peso': row[10],
                    'volumen': row[11],
                }
                visitaSerializador = RutVisitaSerializador(data=data)
                if visitaSerializador.is_valid():
                    visitaSerializador.save()
                else:
                    return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': visitaSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'mensaje':'Se importo el archivo con exito'}, status=status.HTTP_200_OK)        
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], url_path=r'decodificar',)
    def decodificar(self, request):
        guias = RutVisita.objects.filter(decodificado = False)
        if guias.exists():
            direcciones = []
            for guia in guias:
                direcciones.append({
                    'codigo': guia.id,
                    'referencia': guia.guia,
                    'direccion': guia.destinatario_direccion + ', ' + guia.ciudad + ', ' + guia.estado + ', ' + guia.pais
                })
            zinc = Zinc()                        
            respuesta = zinc.decodificar_direccion(direcciones)
            if respuesta['error'] == False: 
                direcciones_respuesta = respuesta['direcciones']
                for direccion in direcciones_respuesta:
                    guia = RutVisita.objects.filter(pk=direccion['codigo']).first()
                    if guia:
                        guia.decodificado = True
                        if direccion['decodificado']:
                            guia.latitud = direccion['latitud']
                            guia.longitud = direccion['longitud']
                        else:
                            guia.decodificado_error = True
                        guia.save()
                return Response({'mensaje': 'Proceso exitoso'}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje': f"{respuesta['mensaje']}", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'mensaje': 'No hay guias pendientes por decodificar'}, status=status.HTTP_200_OK) 
        
    @action(detail=False, methods=["post"], url_path=r'ordenar',)
    def ordenar(self, request):
        visitas = RutVisita.objects.all()
        if visitas.exists():
            lat_inicial = 6.197023
            lon_inicial = -75.585760
            visitas_ordenadas = ordenar_ruta(visitas, lat_inicial, lon_inicial)            
            serializer = self.get_serializer(visitas_ordenadas, many=True)            
            return Response({'visitas_ordenadas': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'mensaje': 'No hay visitas pendientes por ordenar'}, status=status.HTTP_200_OK) 
        
    @action(detail=False, methods=["post"], url_path=r'rutear',)
    def rutear(self, request):
        visitas = RutVisita.objects.filter(estado_despacho = False).order_by('orden')
        if visitas.exists():
            vehiculos = RutVehiculo.objects.all()
            if vehiculos.exists():
                for vehiculo in vehiculos:
                    peso_total = 0
                    volumen_total = 0
                    cantidad_visitas = 0
                    despacho = RutDespacho()
                    despacho.fecha = timezone.now()
                    despacho.vehiculo = vehiculo
                    despacho.save()
                    for visita in visitas:
                        peso_total += visita.peso
                        volumen_total += visita.volumen
                        cantidad_visitas += 1
                        visita.estado_despacho = True
                        visita.despacho = despacho
                        visita.save()
                    despacho.peso = peso_total
                    despacho.volumen = volumen_total
                    despacho.visitas = cantidad_visitas
                    despacho.save()
                return Response({'mensaje': 'Se crean las rutas exitosamente'}, status=status.HTTP_200_OK)                
            else:
                return Response({'mensaje': 'No hay vehculos disponibles'}, status=status.HTTP_400_BAD_REQUEST)                     
        else:
            return Response({'mensaje': 'No hay visitas pendientes por rutear'}, status=status.HTTP_400_BAD_REQUEST)

               