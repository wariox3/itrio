from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ruteo.models.visita import RutVisita
from ruteo.models.despacho import RutDespacho
from ruteo.models.vehiculo import RutVehiculo
from ruteo.models.franja import RutFranja
from ruteo.models.flota import RutFlota
from general.models.ciudad import GenCiudad
from contenedor.models import CtnDireccion
from ruteo.serializers.visita import RutVisitaSerializador
import base64
from io import BytesIO
import openpyxl
from datetime import datetime
from django.utils import timezone
from utilidades.zinc import Zinc
from utilidades.holmio import Holmio
from utilidades.google import Google
from shapely.geometry import Point, Polygon
from math import radians, cos, sin, asin, sqrt
from django.db.models import Sum, F, Count
from django.db.models.functions import Coalesce
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import re
import gc

def calcular_distancia(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Fórmula de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

# Resolver el problema del viajante (TSP) para determinar la ruta óptima
def tsp_ruta(inicio, distancias):
    n = len(distancias)
    visited = [False] * n
    ruta = [inicio]
    visited[inicio] = True

    for _ in range(n - 1):
        last = ruta[-1]
        next_city = min(
            (i for i in range(n) if not visited[i]),
            key=lambda i: distancias[last][i]
        )
        ruta.append(next_city)
        visited[next_city] = True
    return ruta

def ubicar_punto(franjas, latitud, longitud):    
    for franja in franjas:
        coordenadas = [(coord['lng'], coord['lat']) for coord in franja.coordenadas]
        poligono = Polygon(coordenadas)                
        punto = Point(longitud, latitud)
        if poligono.contains(punto):
            return {'encontrado': True, 'franja': {'id':franja.id, 'codigo':franja.codigo}}
    return {'encontrado': False }

class RutVisitaViewSet(viewsets.ModelViewSet):
    queryset = RutVisita.objects.all()
    serializer_class = RutVisitaSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'importar-excel',)
    def importar_excel(self, request):
        raw = request.data
        archivo_base64 = raw.get('archivo_base64')
        if archivo_base64:
            archivo_data = base64.b64decode(archivo_base64)
            archivo = BytesIO(archivo_data)
            wb = openpyxl.load_workbook(archivo)
            sheet = wb.active    
            data_modelo = []
            errores = False
            errores_datos = []    
            franjas = RutFranja.objects.all()
            google = Google()
            total_registros = sheet.max_row - 1
            if total_registros <= 1000:
                for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):                
                    if len(row) < 14:
                        return Response({'mensaje':'El archivo no tiene la estructura requerida', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                    fecha_texto = str(row[1])
                    try:                                        
                        fecha = datetime.strptime(fecha_texto, '%Y%m%d')
                    except ValueError:
                        fecha = None
                    
                    documento = str(row[2])
                    direccion_destinatario = row[4] or ""
                    direccion_destinatario = direccion_destinatario.replace("\t", "").replace("\n", "")
                    direccion_destinatario = re.sub(r'[\s\u2000-\u200F\u3000\u31A0]+', ' ', direccion_destinatario).strip()   
                    direccion_destinatario = re.sub(r'[\s\u2000-\u200F\u3000\u3164]+', ' ', direccion_destinatario).strip()                 
                    direccion_destinatario = re.sub(r'\s+', ' ', direccion_destinatario.strip())                    
                    direccion_destinatario = direccion_destinatario[:150]
                    telefono_destinatario = str(row[6])
                    if telefono_destinatario:
                        telefono_destinatario[:50]
                    decodificado = False
                    if row[12] == 1 or row[12] == "1":
                        decodificado = True

                    data = {
                        'numero': row[0],
                        'fecha':fecha,
                        'documento': documento[:30],
                        'destinatario': row[3],
                        'destinatario_direccion': direccion_destinatario,
                        'ciudad': row[5],
                        'destinatario_telefono': telefono_destinatario,
                        'destinatario_correo': row[7],
                        'peso': row[8],
                        'volumen': row[9],
                        'latitud': row[10],
                        'longitud': row[11],
                        'estado_decodificado': decodificado,
                        'tiempo_servicio': row[13],
                        'estado_franja': False,
                        'franja': None
                    }
                    if decodificado == False: 
                        if direccion_destinatario:                   
                            direccion = CtnDireccion.objects.filter(direccion=direccion_destinatario).first()
                            if direccion:
                                decodificado = True    
                                data['estado_decodificado'] = True            
                                data['latitud'] = direccion.latitud                        
                                data['longitud'] = direccion.longitud
                                data['destinatario_direccion_formato'] = direccion.direccion_formato
                                if direccion.cantidad_resultados > 1:
                                    data['estado_decodificado_alerta'] = True                                
                            else:
                                respuesta = google.decodificar_direccion(data['destinatario_direccion'])
                                if respuesta['error'] == False:
                                    decodificado = True    
                                    data['estado_decodificado'] = True            
                                    data['latitud'] = respuesta['latitud']
                                    data['longitud'] = respuesta['longitud']
                                    data['destinatario_direccion_formato'] = respuesta['direccion_formato']
                                    if respuesta['cantidad_resultados'] > 1:
                                        data['estado_decodificado_alerta'] = True
                    if data['estado_decodificado'] == True:
                        respuesta = ubicar_punto(franjas, data['latitud'], data['longitud'])
                        if respuesta['encontrado']:
                            data['franja'] = respuesta['franja']['id']
                            data['estado_franja'] = True
                        else:
                            data['estado_franja'] = False
                    serializer = RutVisitaSerializador(data=data)
                    if serializer.is_valid():
                        data_modelo.append(serializer.validated_data)
                    else:
                        errores = True
                        error_dato = {
                            'fila': i,
                            'errores': serializer.errors
                        }
                        errores_datos.append(error_dato)
                if not errores:
                    for detalle in data_modelo:
                        RutVisita.objects.create(**detalle)
                    gc.collect()
                    return Response({'mensaje': 'Se importó el archivo con éxito'}, status=status.HTTP_200_OK)
                else:
                    gc.collect()                    
                    return Response({'mensaje':'Errores de validacion', 'codigo':1, 'errores_validador': errores_datos}, status=status.HTTP_400_BAD_REQUEST)                                    
            else:
                return Response({'mensaje':'Solo se permiten importar hasta 1000 registros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path=r'importar-complemento',)
    def importar_complemento(self, request):
        raw = request.data 
        limite = raw.get('limite', 1)
        guia_desde = raw.get('guia_desde', None)
        guia_hasta = raw.get('guia_hasta', None)
        pendiente_despacho = raw.get('pendiente_despacho', None)
        parametros = {
            'limite': limite,
            'guia_desde': guia_desde,
            'guia_hasta': guia_hasta,
            'pendiente_despacho': pendiente_despacho
        }
        franjas = RutFranja.objects.all()
        cantidad = 0       
        google = Google() 
        holmio = Holmio()
        respuesta = holmio.ruteoPendiente(parametros)
        if respuesta['error'] == False:                                   
            guias = respuesta['guias']
            for guia in guias:                                                                        
                direccion_destinatario = f"{guia['direccionDestinatario']}, {guia['ciudadDestinoNombre']}" or ""
                direccion_destinatario = direccion_destinatario.replace("\t", "").replace("\n", "")
                direccion_destinatario = re.sub(r'[\s\u2000-\u200F\u3000\u31A0]+', ' ', direccion_destinatario).strip()   
                direccion_destinatario = re.sub(r'[\s\u2000-\u200F\u3000\u3164]+', ' ', direccion_destinatario).strip()                 
                direccion_destinatario = re.sub(r'\s+', ' ', direccion_destinatario.strip())
                direccion_destinatario = direccion_destinatario[:150]                                                
                fecha = datetime.fromisoformat(guia['fechaIngreso'])  
                nombre_destinatario = (guia['nombreDestinatario'][:150] if guia['nombreDestinatario'] is not None and guia['nombreDestinatario'] != "" else None)                                                
                documentoCliente = (guia['documentoCliente'][:30] if guia['documentoCliente'] is not None and guia['documentoCliente'] != "" else None)
                telefono_destinatario = (guia['telefonoDestinatario'][:50] if guia['telefonoDestinatario'] is not None and guia['telefonoDestinatario'] != "" else None)
                data = {
                    'guia': guia['codigoGuiaPk'],
                    'fecha':fecha,
                    'documento': documentoCliente,
                    'destinatario': nombre_destinatario,
                    'destinatario_direccion': direccion_destinatario,
                    'ciudad': None,
                    'destinatario_telefono': telefono_destinatario,
                    'destinatario_correo': None,
                    'peso': guia['pesoReal'] or 0,
                    'volumen': guia['pesoVolumen'] or 0,
                    'latitud': None,
                    'longitud': None,
                    'tiempo_servicio': 3,
                    'estado_decodificado': False,
                    'estado_franja': False,
                    'franja': None
                }

                                          
                direccion = CtnDireccion.objects.filter(direccion=direccion_destinatario).first()
                if direccion:    
                    data['estado_decodificado'] = True            
                    data['latitud'] = direccion.latitud                        
                    data['longitud'] = direccion.longitud
                    data['destinatario_direccion_formato'] = direccion.direccion_formato
                else:
                    respuesta = google.decodificar_direccion(data['destinatario_direccion'])
                    if respuesta['error'] == False:                        
                        data['estado_decodificado'] = True            
                        data['latitud'] = respuesta['latitud']
                        data['longitud'] = respuesta['longitud']
                        data['destinatario_direccion_formato'] = respuesta['direccion_formato']
                
                if data['estado_decodificado'] == True:
                    respuesta = ubicar_punto(franjas, data['latitud'], data['longitud'])
                    if respuesta['encontrado']:
                        data['franja'] = respuesta['franja']['id']
                        data['estado_franja'] = True
                    else:
                        data['estado_franja'] = False
                visitaSerializador = RutVisitaSerializador(data=data)
                if visitaSerializador.is_valid():
                    visitaSerializador.save()
                    cantidad += 1                                                                                    
                else:
                    return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': visitaSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)                              
            return Response({'mensaje':f'Se importaron {cantidad} las guias con exito'}, status=status.HTTP_200_OK)
        else:
            return Response({'mensaje':f'Error en la conexion: {respuesta["mensaje"]}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'decodificar',)
    def decodificar(self, request):
        visitas = RutVisita.objects.filter(estado_decodificado = None)[:1]
        if visitas.exists():            
            datosVisitas = []           
            for visita in visitas:  
                if visita.destinatario_direccion:
                    datosVisita = {
                        "cuenta": "1",
                        "modelo": "guia",
                        "canal": 3,
                        "codigo": visita.id,
                        "direccion": visita.destinatario_direccion,
                        "ciudad": visita.ciudad_id,
                        "principal": False,                
                    }    
                    datosVisitas.append(datosVisita)                
            if datosVisitas:
                datos = {
                    "lote": datosVisitas
                }
                #zinc = Zinc()
                #respuesta = zinc.decodificar_direccion_lote(datos)
                '''if respuesta['error'] == False:                     
                    datos = respuesta['datos']
                    visita.estado_decodificado = datos['decodificado']                                                                                                   
                    visita.latitud = datos['latitud']
                    visita.longitud = datos['longitud']                    
                    visita.save()'''
            return Response({'mensaje': 'Proceso exitoso'}, status=status.HTTP_200_OK)
        else:
            return Response({'mensaje': 'No hay guias pendientes por decodificar'}, status=status.HTTP_200_OK) 

    @action(detail=False, methods=["post"], url_path=r'decodificar-externo',)
    def decodificar_externo(self, request):
        raw = request.data 
        guia_id = raw.get('guia_id')
        direccion = raw.get('direccion')
        ciudad_id = raw.get('ciudad_id')
        decodificar_principal = raw.get('decodificar_principal', False)
        if guia_id and direccion and ciudad_id:
            try:
                ciudad = GenCiudad.objects.get(pk=ciudad_id)
                zinc = Zinc()                                      
                datos = {
                    "cuenta": "1",
                    "modelo": "guia",
                    "canal": 3,
                    "codigo": guia_id,
                    "direccion": direccion,
                    "ciudad": ciudad_id,
                    "decodificarPrincipal": decodificar_principal,                
                }
                respuesta = zinc.decodificar_direccion(datos)
                if respuesta['error'] == False:                     
                    datos = respuesta['datos']
                    codigo_franja = ""
                    franjas = RutFranja.objects.all()
                    respuesta = ubicar_punto(franjas, datos['latitud'], datos['longitud'])
                    if respuesta['encontrado']:
                        codigo_franja = respuesta['franja']['codigo']                 
                    datosRespuesta = {
                        "decodificado": datos['decodificado'],
                        "latitud": datos['latitud'],
                        "longitud": datos['longitud'],
                        "franja": codigo_franja
                    }
                    return Response(datosRespuesta, status=status.HTTP_200_OK) 
                else:
                    return Response({'mensaje': f"{respuesta['mensaje']}", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)  
            except GenCiudad.DoesNotExist:
                return Response({'mensaje':'La ciudad no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                      
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'ordenar',)
    def ordenar(self, request):        
        visitas = RutVisita.objects.filter(estado_despacho=False, estado_decodificado=True).values('id', 'latitud', 'longitud')
        if visitas.exists():
            num_locations = len(visitas)

            distance_matrix = [[
                calcular_distancia(loc1['latitud'], loc1['longitud'], loc2['latitud'], loc2['longitud'])
                for loc2 in visitas
            ] for loc1 in visitas]

            # Configurar el problema de enrutamiento
            manager = pywrapcp.RoutingIndexManager(num_locations, 1, 0)
            routing = pywrapcp.RoutingModel(manager)

            # Función de costo
            def distance_callback(from_index, to_index):
                from_node = manager.IndexToNode(from_index)
                to_node = manager.IndexToNode(to_index)
                return distance_matrix[from_node][to_node]

            transit_callback_index = routing.RegisterTransitCallback(distance_callback)
            routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

            # Resolver el problema
            search_parameters = pywrapcp.DefaultRoutingSearchParameters()
            search_parameters.first_solution_strategy = (
                routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
            solution = routing.SolveWithParameters(search_parameters)

            if solution:
                # Extraer la ruta optimizada y asignar el orden
                route = []
                index = routing.Start(0)
                while not routing.IsEnd(index):
                    route.append(manager.IndexToNode(index))
                    index = solution.Value(routing.NextVar(index))

                # Actualizar el orden en la base de datos
                for order, visit_index in enumerate(route):
                    visita_id = visitas[visit_index]['id']
                    RutVisita.objects.filter(id=visita_id).update(orden=order + 1)

            return Response({'mensaje':'visitas ordenadas'}, status=status.HTTP_200_OK)
        else:
            return Response({'mensaje': 'No hay visitas pendientes por ordenar'}, status=status.HTTP_200_OK) 

    @action(detail=False, methods=["post"], url_path=r'ordenar-google',)
    def ordenar_google(self, request):        
        visitas = RutVisita.objects.filter(estado_despacho=False, estado_decodificado=True).values('id', 'latitud', 'longitud')
        if visitas.exists():
            ubicacion_inicial = (6.197023, -75.585760)
            visitas_ubicaciones = [ubicacion_inicial] + [(visita['latitud'], visita['longitud']) for visita in visitas]
            gogle = Google()
            resultado = gogle.matriz_distancia(visitas_ubicaciones)
            if not resultado["error"]:  
                distancias = resultado['distancias']
                duraciones = resultado['duraciones']                                
                ruta = tsp_ruta(0, distancias)
                visitas_ordenadas = []
                for orden, i in enumerate(ruta):
                    if i == 0:  # Ubicación inicial no tiene id
                        visitas_ordenadas.append({
                            "id": None,
                            "latitud": visitas_ubicaciones[i][0],
                            "longitud": visitas_ubicaciones[i][1],
                            "orden": orden,
                            "tiempo_hasta_proxima": None,
                            "distancia_hasta_proxima": None
                        })
                    else:
                        visita = visitas[i - 1]
                        tiempo_hasta_proxima = None
                        distancia_hasta_proxima = None
                        if orden < len(ruta) - 1:  # Si no es la última visita
                            tiempo_hasta_proxima = duraciones[i][ruta[orden + 1]]
                            distancia_hasta_proxima = distancias[i][ruta[orden + 1]]
                        visitas_ordenadas.append({
                            "id": visita['id'],
                            "latitud": visitas_ubicaciones[i][0],
                            "longitud": visitas_ubicaciones[i][1],
                            "orden": orden,
                            "tiempo_hasta_proxima": tiempo_hasta_proxima,
                            "distancia_hasta_proxima": distancia_hasta_proxima
                        })                    
                        RutVisita.objects.filter(id=visita['id']).update(orden=orden)                       
                return Response({'mensaje':'visitas ordenadas', 'datos': visitas_ordenadas}, status=status.HTTP_200_OK)
            else:                
                return Response({'mensaje':resultado["mensaje"], 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                   
        else:
            return Response({'mensaje': 'No hay visitas pendientes por ordenar'}, status=status.HTTP_200_OK) 

    @action(detail=False, methods=["post"], url_path=r'rutear',)
    def rutear(self, request):
        flota = RutFlota.objects.all()        
        if flota.exists():
            visitas = RutVisita.objects.filter(estado_despacho = False).order_by('orden')                            
            cantidad_vehiculos = len(flota)
            vehiculo_indice = 0
            vehiculo = flota[vehiculo_indice].vehiculo            
            peso_total = 0  
            crear_despacho = True
            for visita in visitas:
                if peso_total + visita.peso > vehiculo.capacidad:
                    asignado = False
                    peso_total = 0
                    while vehiculo_indice + 1 <= cantidad_vehiculos and asignado == False:                         
                        vehiculo_indice += 1
                        vehiculo = flota[vehiculo_indice].vehiculo
                        if peso_total + visita.peso <= vehiculo.capacidad:                             
                            crear_despacho = True
                            asignado = True
                    if vehiculo_indice + 1 > cantidad_vehiculos:
                        break
                
                if crear_despacho:
                    despacho = RutDespacho()
                    despacho.fecha = timezone.now()
                    despacho.vehiculo = vehiculo
                    despacho.peso = despacho.peso + visita.peso
                    despacho.visitas = despacho.visitas + 1
                    despacho.save()
                    crear_despacho = False
                else:
                    despacho.peso = despacho.peso + visita.peso
                    despacho.visitas = despacho.visitas + 1
                    despacho.save()        
                peso_total += visita.peso
                visita.estado_despacho = True
                visita.despacho = despacho
                visita.save()
            return Response({'mensaje': 'Se crean las rutas exitosamente'}, status=status.HTTP_200_OK)                
        else:
            return Response({'mensaje': 'No hay visitas pendientes por rutear o vehiculos disponibles'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], url_path=r'ubicar',)
    def ubicar(self, request):             
        raw = request.data
        cantidad = 0
        franjas = RutFranja.objects.all()
        visitas = RutVisita.objects.filter(estado_franja = None)
        for visita in visitas:
            respuesta = ubicar_punto(franjas, visita.latitud, visita.longitud)
            if respuesta['encontrado']:
                visita.franja_id = respuesta['franja']['id']
                visita.estado_franja = True
            else:
                visita.estado_franja = False
            visita.save()  
            cantidad += 1      
        return Response({'mensaje': f'Se asignó franja a {cantidad} de visitas'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path=r'ubicar-punto',)
    def ubicar_punto(self, request):             
        raw = request.data
        latitud = raw.get('latitud')
        longitud = raw.get('longitud')           
        if latitud and longitud:
            franjas = RutFranja.objects.all()
            respuesta = ubicar_punto(franjas, latitud, longitud)
            return Response(respuesta, status=status.HTTP_200_OK)                                                    
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)  

    @action(detail=False, methods=["post"], url_path=r'eliminar-todos',)
    def eliminar_todos(self, request):             
        raw = request.data
        estado_decodificado = raw.get('estado_decodificado', None)
        if estado_decodificado == False:
            RutVisita.objects.filter(estado_decodificado=False).delete()
        else:
            RutVisita.objects.filter(estado_despacho=False).delete()
        return Response({'mensaje':'eliminados'}, status=status.HTTP_200_OK) 

    @action(detail=False, methods=["post"], url_path=r'resumen',)
    def resumen(self, request):
        visitas = RutVisita.objects.filter(estado_despacho = False).aggregate(
            cantidad=Count('id'), 
            peso=Coalesce(Sum('peso'), 0.0)
            )     
        errores = RutVisita.objects.filter(estado_despacho = False, estado_decodificado=False).aggregate(
            cantidad=Count('id'))
        alertas = RutVisita.objects.filter(estado_despacho = False, estado_decodificado_alerta=True).aggregate(
            cantidad=Count('id'))        
        return Response({'resumen': visitas, 'errores': errores, 'alertas':alertas}, status=status.HTTP_200_OK)                                                                      