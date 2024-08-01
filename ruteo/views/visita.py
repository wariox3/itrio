from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ruteo.models.visita import RutVisita
from ruteo.models.despacho import RutDespacho
from ruteo.models.vehiculo import RutVehiculo
from ruteo.serializers.visita import RutVisitaSerializador
import base64
from io import BytesIO
import openpyxl
from datetime import datetime
from django.utils import timezone
from utilidades.zinc import Zinc
from math import radians, cos, sin, asin, sqrt

def listar(desplazar, limite, limiteTotal, filtros, ordenamientos):
    visitas = RutVisita.objects.all()
    if filtros:
        for filtro in filtros:
            visitas = visitas.filter(**{filtro['propiedad']: filtro['valor1']})
    if ordenamientos:
        visitas = visitas.order_by(*ordenamientos)              
    visitas = visitas[desplazar:limite+desplazar]
    itemsCantidad = RutVisita.objects.all()[:limiteTotal].count()                   
    respuesta = {'visitas': visitas, "cantidad_registros": itemsCantidad}
    return respuesta 

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

    @action(detail=False, methods=["post"], url_path=r'lista',)
    def lista(self, request):
        raw = request.data
        desplazar = raw.get('desplazar', 0)
        limite = raw.get('limite', 50)    
        limiteTotal = raw.get('limite_total', 5000)                
        ordenamientos = raw.get('ordenamientos', [])            
        filtros = raw.get('filtros', [])                   
        respuesta = listar(desplazar, limite, limiteTotal, filtros, ordenamientos)     
        serializador = RutVisitaSerializador(respuesta['visitas'], many=True)
        visitas = serializador.data
        return Response(visitas, status=status.HTTP_200_OK)

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
                decodificado = False
                if row[14] == 1:
                    decodificado = True
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
                    'latitud': row[12],
                    'longitud': row[13],
                    'decodificado': decodificado
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
        vehiculos = RutVehiculo.objects.filter(estado_asignado = False, estado_activo = True).order_by('id')
        visitas = RutVisita.objects.filter(estado_despacho = False).order_by('orden')
        if visitas.exists() and vehiculos.exists():
            cantidad_vehiculos = len(vehiculos)
            posicion_vehiculo = 0
            vehiculo = vehiculos[posicion_vehiculo]
            peso_total = 0  
            flota_insuficiente = False
            crear_despacho = True
            for visita in visitas:
                if peso_total + visita.peso > vehiculo.capacidad:
                    asignado = False
                    peso_total = 0
                    while posicion_vehiculo + 2 <= cantidad_vehiculos and asignado == False:                         
                        posicion_vehiculo += 1
                        vehiculo = vehiculos[posicion_vehiculo]
                        if peso_total + visita.peso <= vehiculo.capacidad:                             
                            crear_despacho = True
                            asignado = True
                    if posicion_vehiculo + 2 > cantidad_vehiculos:
                        flota_insuficiente = True
                        break
                
                if crear_despacho:
                    despacho = RutDespacho()
                    despacho.fecha = timezone.now()
                    despacho.vehiculo = vehiculo
                    despacho.peso = despacho.peso + visita.peso
                    despacho.visitas = despacho.visitas + 1
                    despacho.save()
                    vehiculo.estado_asignado = True
                    vehiculo.save()
                    crear_despacho = False
                else:
                    despacho.peso = despacho.peso + visita.peso
                    despacho.visitas = despacho.visitas + 1
                    despacho.save()        
                peso_total += visita.peso
                visita.estado_despacho = True
                visita.despacho = despacho
                visita.save()
            return Response({'mensaje': 'Se crean las rutas exitosamente', 'flota_insuficiente': flota_insuficiente}, status=status.HTTP_200_OK)                
        else:
            return Response({'mensaje': 'No hay visitas pendientes por rutear o vehiculos disponibles'}, status=status.HTTP_400_BAD_REQUEST)

               