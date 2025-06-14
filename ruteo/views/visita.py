from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ruteo.models.visita import RutVisita
from ruteo.models.despacho import RutDespacho
from ruteo.models.vehiculo import RutVehiculo
from ruteo.models.franja import RutFranja
from ruteo.models.flota import RutFlota
from general.models.configuracion import GenConfiguracion
from general.models.ciudad import GenCiudad
from general.models.archivo import GenArchivo
from contenedor.models import CtnDireccion
from ruteo.serializers.visita import RutVisitaSerializador
from datetime import datetime
from django.utils import timezone
from utilidades.holmio import Holmio
from utilidades.google import Google
from utilidades.backblaze import Backblaze
from utilidades.imagen import Imagen
from shapely.geometry import Point, Polygon
from math import radians, cos, sin, asin, sqrt, atan2
from django.db.models import Sum, F, Count
from django.db.models.functions import Coalesce
from django.db import transaction
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from io import BytesIO
from decimal import Decimal, ROUND_HALF_UP
import re
import gc
import base64
import openpyxl
import numpy as np
import json





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

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radio de la Tierra en kilómetros
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  # Retorna la distancia en kilómetros

def construir_matriz_distancias(visitas, punto_inicial):
    n = len(visitas)
    matriz = np.zeros((n + 1, n + 1))  # +1 para incluir el punto de partida
    puntos = [(punto_inicial['latitud'], punto_inicial['longitud'])] + [(v['latitud'], v['longitud']) for v in visitas]

    for i in range(n + 1):
        for j in range(n + 1):
            matriz[i][j] = haversine(puntos[i][0], puntos[i][1], puntos[j][0], puntos[j][1])
    
    return matriz

def json_texto(texto):
    if not texto or not texto.strip():
        return None        
    try:
        datos = json.loads(texto)
        return datos if isinstance(datos, dict) else None
    except (json.JSONDecodeError, ValueError):
        return None

class RutVisitaViewSet(viewsets.ModelViewSet):
    queryset = RutVisita.objects.all()
    serializer_class = RutVisitaSerializador
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):        
        visita = self.get_object()
        if visita.despacho_id:
                despacho = RutDespacho.objects.get(pk=visita.despacho_id)                
                if despacho.estado_aprobado == True:
                    return Response({'mensaje': 'No se puede eliminar la visita porque el despacho esta aprobado.'}, status=status.HTTP_400_BAD_REQUEST)        
                else:
                    despacho.peso = despacho.peso - visita.peso
                    despacho.volumen = despacho.volumen - visita.volumen
                    despacho.visitas -= 1
                    despacho.save()        
        self.perform_destroy(visita)
        return Response(status=status.HTTP_204_NO_CONTENT) 

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
                    direccion_destinatario = self.limpiar_direccion(row[4])
                    telefono_destinatario = str(row[6])
                    if telefono_destinatario:
                        telefono_destinatario[:50]                    
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
                        'latitud': None,
                        'longitud': None,
                        'estado_decodificado': False,
                        'tiempo_servicio': row[13],
                        'estado_franja': False,
                        'franja': None,
                        'resultados': None
                    }                 
                    if direccion_destinatario:                   
                        direccion = CtnDireccion.objects.filter(direccion=direccion_destinatario).first()
                        if direccion:
                            data['estado_decodificado'] = True            
                            data['latitud'] = direccion.latitud                        
                            data['longitud'] = direccion.longitud
                            data['destinatario_direccion_formato'] = direccion.direccion_formato
                            data['resultados'] = direccion.resultados
                            if direccion.cantidad_resultados > 1:
                                data['estado_decodificado_alerta'] = True                                
                        else:
                            respuesta = google.decodificar_direccion(data['destinatario_direccion'])
                            if respuesta['error'] == False:   
                                data['estado_decodificado'] = True            
                                data['latitud'] = respuesta['latitud']
                                data['longitud'] = respuesta['longitud']
                                data['destinatario_direccion_formato'] = respuesta['direccion_formato']
                                data['resultados'] = respuesta['resultados']
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
                    self.ubicar(request)
                    self.ordenar(request)
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
        fecha_desde = raw.get('fecha_desde', None)
        fecha_hasta = raw.get('fecha_hasta', None)        
        pendiente_despacho = raw.get('pendiente_despacho', None)
        codigo_contacto = raw.get('codigo_contacto', None)
        codigo_destino = raw.get('codigo_destino', None)
        codigo_zona = raw.get('codigo_zona', None)
        parametros = {
            'limite': limite,
            'guia_desde': guia_desde,
            'guia_hasta': guia_hasta,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'pendiente_despacho': pendiente_despacho,
            'codigo_contacto': codigo_contacto,
            'codigo_destino' : codigo_destino,
            'codigo_zona': codigo_zona
        }
        franjas = RutFranja.objects.all()
        cantidad = 0       
        google = Google() 
        holmio = Holmio()
        respuesta = holmio.ruteo_pendiente(parametros)
        if respuesta['error'] == False:                                   
            guias = respuesta['guias']
            for guia in guias:                                                                        
                direccion_destinatario = self.limpiar_direccion(guia['direccionDestinatario'])                                               
                fecha = datetime.fromisoformat(guia['fechaIngreso'])  
                nombre_destinatario = (guia['nombreDestinatario'][:150] if guia['nombreDestinatario'] is not None and guia['nombreDestinatario'] != "" else None)                                                
                documentoCliente = (guia['documentoCliente'][:30] if guia['documentoCliente'] is not None and guia['documentoCliente'] != "" else None)
                telefono_destinatario = (guia['telefonoDestinatario'][:50] if guia['telefonoDestinatario'] is not None and guia['telefonoDestinatario'] != "" else None)
                data = {
                    'numero': guia['codigoGuiaPk'],
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
                    'estado_decodificado': False,
                    'tiempo_servicio': 3,
                    'estado_franja': False,
                    'franja': None,
                    'resultados': None
                } 
                if direccion_destinatario:                   
                    direccion = CtnDireccion.objects.filter(direccion=direccion_destinatario).first()
                    if direccion:
                        data['estado_decodificado'] = True            
                        data['latitud'] = direccion.latitud                        
                        data['longitud'] = direccion.longitud
                        data['destinatario_direccion_formato'] = direccion.direccion_formato
                        data['resultados'] = direccion.resultados
                        if direccion.cantidad_resultados > 1:
                            data['estado_decodificado_alerta'] = True                                
                    else:
                        respuesta = google.decodificar_direccion(data['destinatario_direccion'])
                        if respuesta['error'] == False:   
                            data['estado_decodificado'] = True            
                            data['latitud'] = respuesta['latitud']
                            data['longitud'] = respuesta['longitud']
                            data['destinatario_direccion_formato'] = respuesta['direccion_formato']
                            data['resultados'] = respuesta['resultados']
                            if respuesta['cantidad_resultados'] > 1:
                                data['estado_decodificado_alerta'] = True                                          
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
            self.ubicar(request)
            self.ordenar(request)
            return Response({'mensaje':f'Se importaron {cantidad} las guias con exito'}, status=status.HTTP_200_OK)
        else:
            return Response({'mensaje':f'Error en la conexion: {respuesta["mensaje"]}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'decodificar',)
    def decodificar_action(self, request):
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

    @action(detail=False, methods=["post"], url_path=r'ordenar_deprecated',)
    def ordenar_deprecated(self, request):      
        raw = request.data
        visitas_franja = RutVisita.objects.filter(estado_despacho=False, estado_decodificado=True).values('franja_codigo').annotate(cantidad=Count('id'))  
        filtros = raw.get('filtros')        
        if filtros:
            for filtro in filtros:
                visitas_franja = visitas_franja.filter(**{filtro['propiedad']: filtro['valor1']})
        for visita_franja in visitas_franja:                        
            print(visita_franja['franja_codigo'])
            visitas = RutVisita.objects.filter(estado_despacho=False, estado_decodificado=True).values('id', 'latitud', 'longitud', 'tiempo_servicio')
            if visita_franja['franja_codigo']:
                visitas = visitas.filter(franja_codigo=visita_franja['franja_codigo'])
            else:
                visitas = visitas.filter(franja_codigo=None)     
            if visitas.exists():
                cantidad_visitas = len(visitas)                   
                punto_inicial = {'latitud': 6.200479, 'longitud': -75.586350}            
                matriz = construir_matriz_distancias(visitas, punto_inicial)                    
                manager = pywrapcp.RoutingIndexManager(len(matriz), 1, 0)
                routing = pywrapcp.RoutingModel(manager)
                
                # Función de costo
                def distancia_callback(from_index, to_index):
                    from_node = manager.IndexToNode(from_index)
                    to_node = manager.IndexToNode(to_index)
                    return int(matriz[from_node][to_node] * 1000)
                
                transit_callback_index = routing.RegisterTransitCallback(distancia_callback)
                routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)                        
                search_parameters = pywrapcp.DefaultRoutingSearchParameters()
                search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
                
                solution = routing.SolveWithParameters(search_parameters)            
                if not solution:
                    return None

                # Extraer el orden óptimo
                index = routing.Start(0)
                orden = []
                while not routing.IsEnd(index):
                    node = manager.IndexToNode(index)
                    if node != 0:  # Ignorar el punto de partida
                        orden.append(node - 1)  # Ajustar índice
                    index = solution.Value(routing.NextVar(index))

                for idx, visita_idx in enumerate(orden):
                    visita_id = visitas[visita_idx]['id']
                    tiempo_servicio = Decimal(visitas[visita_idx]['tiempo_servicio'])
                    distancia = 0                
                    if idx == 0:
                        # Primera visita: distancia desde el punto inicial
                        distancia = matriz[0][visita_idx + 1]
                    else:
                        # Visitas posteriores: distancia desde la visita anterior
                        anterior_idx = orden[idx - 1]
                        distancia = matriz[anterior_idx + 1][visita_idx + 1]
                    tiempo_trayecto = Decimal(distancia * 1.6)
                    tiempo = tiempo_servicio+tiempo_trayecto            
                    RutVisita.objects.filter(id=visita_id).update(orden=idx + 1, distancia=distancia, tiempo_trayecto=tiempo_trayecto, tiempo=tiempo)                
        return Response({'mensaje':'visitas ordenadas'}, status=status.HTTP_200_OK) 

    @action(detail=False, methods=["post"], url_path=r'ordenar',)
    def ordenar(self, request):      
        raw = request.data
        filtros = raw.get('filtros', [])
        
        # Verificar si hay filtros de franja (ahora buscando 'franja_id')
        tiene_filtro_franja = any(filtro.get('propiedad') == 'franja_id' for filtro in filtros if isinstance(filtro, dict))
        
        if tiene_filtro_franja:
            # Caso 1: Hay filtro de franja - ordenar todas las visitas juntas
            visitas = RutVisita.objects.filter(estado_despacho=False, estado_decodificado=True)
            
            # Aplicar todos los filtros
            for filtro in filtros:
                operador = filtro.get('operador')
                propiedad = filtro['propiedad']
                if operador == 'range':
                    visitas = visitas.filter(**{f'{propiedad}__{operador}': (filtro['valor1'], filtro['valor2'])})
                elif operador:
                    visitas = visitas.filter(**{f'{propiedad}__{operador}': filtro['valor1']})
                else:
                    visitas = visitas.filter(**{propiedad: filtro['valor1']})
            
            visitas = visitas.values('id', 'latitud', 'longitud', 'tiempo_servicio')
            
            if visitas.exists():
                self.ordenar_visitas(visitas)
        else:
            # Caso 2: No hay filtro de franja - ordenar por franja separadamente
            visitas_franja = RutVisita.objects.filter(
                estado_despacho=False, 
                estado_decodificado=True
            ).values('franja_codigo').annotate(cantidad=Count('id'))
            
            # Aplicar otros filtros (excluyendo 'franja_id')
            for filtro in filtros:
                operador = filtro.get('operador')
                propiedad = filtro['propiedad']
                if propiedad != 'franja_id':  # Ahora excluimos filtros de franja_id
                    if operador == 'range':
                        visitas_franja = visitas_franja.filter(**{f'{propiedad}__{operador}': (filtro['valor1'], filtro['valor2'])})
                    elif operador:
                        visitas_franja = visitas_franja.filter(**{f'{propiedad}__{operador}': filtro['valor1']})
                    else:
                        visitas_franja = visitas_franja.filter(**{propiedad: filtro['valor1']})
            
            for visita_franja in visitas_franja:
                visitas = RutVisita.objects.filter(
                    estado_despacho=False, 
                    estado_decodificado=True,
                    franja_codigo=visita_franja['franja_codigo']
                ).values('id', 'latitud', 'longitud', 'tiempo_servicio')
                
                if visitas.exists():
                    self.ordenar_visitas(visitas)
        
        return Response({'mensaje':'visitas ordenadas'}, status=status.HTTP_200_OK)

    def ordenar_visitas(self, visitas):
        """Función auxiliar para ordenar un conjunto de visitas"""
        configuracion = GenConfiguracion.objects.filter(id=1).first()

        if not configuracion or configuracion.rut_latitud is None or configuracion.rut_longitud is None:
            return Response({
                'mensaje': 'Debe configurar punto de origen para poder ordenar las visitas', 
                'codigo': 15
            }, status=status.HTTP_400_BAD_REQUEST)
        
        latitud = float(configuracion.rut_latitud)
        longitud = float(configuracion.rut_longitud)

        punto_inicial = {'latitud': latitud, 'longitud': longitud}         
        matriz = construir_matriz_distancias(visitas, punto_inicial)                    
        manager = pywrapcp.RoutingIndexManager(len(matriz), 1, 0)
        routing = pywrapcp.RoutingModel(manager)
        
        def distancia_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(matriz[from_node][to_node] * 1000)
        
        transit_callback_index = routing.RegisterTransitCallback(distancia_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)                        
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        
        solution = routing.SolveWithParameters(search_parameters)            
        if not solution:
            return None

        index = routing.Start(0)
        orden = []
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            if node != 0:
                orden.append(node - 1)
            index = solution.Value(routing.NextVar(index))

        # Definimos la precisión a 6 decimales
        decimal_6_places = Decimal('0.000001')  # Para redondear a 6 decimales
        
        for idx, visita_idx in enumerate(orden):
            visita_id = visitas[visita_idx]['id']
            
            # Aseguramos que tiempo_servicio no tenga más de 6 decimales
            tiempo_servicio = Decimal(visitas[visita_idx]['tiempo_servicio']).quantize(
                decimal_6_places,
                rounding=ROUND_HALF_UP  # Redondeo estándar (mitad hacia arriba)
            )
            
            distancia = matriz[0][visita_idx + 1] if idx == 0 else matriz[orden[idx - 1] + 1][visita_idx + 1]
            
            # Aseguramos que tiempo_trayecto y tiempo no tengan más de 6 decimales
            tiempo_trayecto = (Decimal(distancia) * Decimal('1.6')).quantize(
                decimal_6_places,
                rounding=ROUND_HALF_UP
            )
            
            tiempo = (tiempo_servicio + tiempo_trayecto).quantize(
                decimal_6_places,
                rounding=ROUND_HALF_UP
            )
            
            RutVisita.objects.filter(id=visita_id).update(
                orden=idx + 1, 
                distancia=distancia, 
                tiempo_trayecto=tiempo_trayecto, 
                tiempo=tiempo
            )

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
        
    @action(detail=False, methods=["post"], url_path=r'rutear_deprecated',)
    def rutear_deprecated(self, request):
        raw = request.data
        filtros = raw.get('filtros')
        flota = RutFlota.objects.filter(vehiculo__estado_asignado=False)
        if flota.exists():
            visitas = RutVisita.objects.filter(estado_despacho=False, estado_devolucion=False, estado_novedad=False)
            if filtros:
                for filtro in filtros:                    
                    operador = filtro.get('operador', None)
                    if operador == 'range':
                        visitas = visitas.filter(**{filtro['propiedad']+'__'+operador: (filtro['valor1'], filtro['valor2'])})
                    else:
                        visitas = visitas.filter(**{filtro['propiedad']+'__'+operador: filtro['valor1']})

            visitas = visitas.order_by('orden')      
            cantidad_vehiculos = flota.count()                                      
            vehiculo_indice = 0
            vehiculo = flota[vehiculo_indice].vehiculo     
            peso_total = 0
            tiempo_total = 0 
            tiempo_servicio_total = 0
            tiempo_trayecto_total = 0 
            crear_despacho = True
            for visita in visitas:
                if peso_total + visita.peso > vehiculo.capacidad or tiempo_total + visita.tiempo > vehiculo.tiempo:
                    asignado = False
                    peso_total = 0
                    tiempo_total = 0 
                    tiempo_servicio_total = 0
                    tiempo_trayecto_total = 0                     
                    while vehiculo_indice + 1 <= cantidad_vehiculos and asignado == False:                         
                        vehiculo_indice += 1                        
                        if vehiculo_indice >= cantidad_vehiculos:
                            asignado = True
                        else: 
                            vehiculo = flota[vehiculo_indice].vehiculo
                            if peso_total + visita.peso <= vehiculo.capacidad or tiempo_total + visita.tiempo <= vehiculo.tiempo:                             
                                crear_despacho = True
                                asignado = True
                    if vehiculo_indice >= cantidad_vehiculos:
                        break                                            

                if crear_despacho:
                    despacho = RutDespacho()
                    despacho.fecha = timezone.now()
                    despacho.vehiculo = vehiculo
                    vehiculo.estado_asignado = True
                    despacho.peso = despacho.peso + visita.peso
                    despacho.volumen = despacho.volumen + visita.volumen
                    despacho.tiempo = despacho.tiempo + visita.tiempo
                    despacho.tiempo_servicio = despacho.tiempo_servicio + visita.tiempo_servicio
                    despacho.tiempo_trayecto = despacho.tiempo_trayecto + visita.tiempo_trayecto
                    despacho.visitas = despacho.visitas + 1
                    despacho.save()
                    vehiculo.save()
                    crear_despacho = False
                else:
                    despacho.peso = despacho.peso + visita.peso
                    despacho.volumen = despacho.volumen + visita.volumen
                    despacho.tiempo = despacho.tiempo + visita.tiempo
                    despacho.tiempo_servicio = despacho.tiempo_servicio + visita.tiempo_servicio
                    despacho.tiempo_trayecto = despacho.tiempo_trayecto + visita.tiempo_trayecto
                    despacho.visitas = despacho.visitas + 1
                    despacho.save()        
                peso_total += visita.peso
                tiempo_total += visita.tiempo
                tiempo_servicio_total += visita.tiempo_servicio
                tiempo_trayecto_total += visita.tiempo_trayecto
                visita.estado_despacho = True
                visita.despacho = despacho
                visita.save()
            return Response({'mensaje': 'Se crean las rutas exitosamente'}, status=status.HTTP_200_OK)                
        else:
            return Response({'mensaje': 'No hay visitas pendientes por rutear o vehiculos disponibles'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'rutear')
    def rutear(self, request):
        raw = request.data
        filtros = raw.get('filtros')

        decimal_6_places = Decimal('0.000001')
        
        configuracion = GenConfiguracion.objects.filter(id=1).first()
        rutear_franja = getattr(configuracion, 'rut_rutear_franja', False)

        flota_disponible = list(
            RutFlota.objects.filter(vehiculo__estado_asignado=False)
            .select_related('vehiculo')
            .order_by('prioridad') 
        )
        if not flota_disponible:
            return Response({'mensaje': 'No hay vehículos disponibles'}, 
                        status=status.HTTP_400_BAD_REQUEST)

        visitas = RutVisita.objects.filter(
            estado_despacho=False, 
            estado_devolucion=False, 
            estado_novedad=False
        )

        if filtros:
            for filtro in filtros:
                operador = filtro.get('operador')
                propiedad = filtro['propiedad']
                if operador == 'range':
                    visitas = visitas.filter(**{f'{propiedad}__{operador}': (filtro['valor1'], filtro['valor2'])})
                elif operador:
                    visitas = visitas.filter(**{f'{propiedad}__{operador}': filtro['valor1']})

        visitas = visitas.order_by('orden')

        visitas_pendientes = list(visitas)
        despachos_creados = 0

        def vehiculo_puede_tomar_visita(vehiculo, visita, peso_actual, tiempo_actual, verificar_franja):
            if (peso_actual + visita.peso > vehiculo.capacidad or 
                tiempo_actual + visita.tiempo > vehiculo.tiempo):
                return False
            
            if not verificar_franja:
                return True
                
            return vehiculo.franjas.filter(id=visita.franja_id).exists()

        if rutear_franja:
            for flota_item in flota_disponible:
                vehiculo = flota_item.vehiculo
                peso_total = 0
                tiempo_total = 0
                despacho = None

                # Procesar solo si el vehículo no está ya asignado
                if vehiculo.estado_asignado:
                    continue

                # Intentar asignar todas las visitas posibles a este vehículo
                for visita in list(visitas_pendientes):
                    if vehiculo_puede_tomar_visita(vehiculo, visita, peso_total, tiempo_total, True):
                        if despacho is None:
                            despacho = RutDespacho.objects.create(
                                fecha=timezone.now(),
                                vehiculo=vehiculo,
                                peso=visita.peso,
                                volumen=visita.volumen,
                                tiempo=visita.tiempo,
                                tiempo_servicio=visita.tiempo_servicio,
                                tiempo_trayecto=visita.tiempo_trayecto,
                                visitas=1
                            )
                            vehiculo.estado_asignado = True
                            vehiculo.save()
                            despachos_creados += 1
                        else:
                            despacho.peso += visita.peso
                            despacho.volumen += visita.volumen
                            despacho.tiempo = (Decimal(despacho.tiempo) + Decimal(visita.tiempo)).quantize(
                                decimal_6_places,
                                rounding=ROUND_HALF_UP
                            )
                            despacho.tiempo_servicio = (Decimal(despacho.tiempo_servicio) + Decimal(visita.tiempo_servicio)).quantize(
                                decimal_6_places,
                                rounding=ROUND_HALF_UP
                            )
                            despacho.tiempo_trayecto = (Decimal(despacho.tiempo_trayecto) + Decimal(visita.tiempo_trayecto)).quantize(
                                decimal_6_places,
                                rounding=ROUND_HALF_UP
                            )
                            despacho.visitas += 1
                            despacho.save()

                        peso_total += visita.peso
                        tiempo_total += visita.tiempo
                        
                        visita.estado_despacho = True
                        visita.despacho = despacho
                        visita.save()
                        
                        visitas_pendientes.remove(visita)

                if visitas_pendientes:
                    continue
                else:
                    break 

            mensaje = (
                f"Operación completada: {despachos_creados} rutas creadas"
                + (f"Pendientes: {len(visitas_pendientes)} visitas (IDs: {', '.join(str(v.id) for v in visitas_pendientes)})" 
                if visitas_pendientes else "")
            )
            return Response({
                'mensaje': mensaje,
                'status': status.HTTP_200_OK
            })

        else:
            vehiculo_index = 0
            while vehiculo_index < len(flota_disponible) and visitas_pendientes:
                flota_item = flota_disponible[vehiculo_index]
                vehiculo = flota_item.vehiculo
                
                if vehiculo.estado_asignado:
                    vehiculo_index += 1
                    continue
                    
                peso_total = 0
                tiempo_total = 0
                despacho = None
                visitas_asignadas_este_vehiculo = 0

                # Hacer copia para iterar seguramente mientras removemos
                for visita in list(visitas_pendientes):
                    if vehiculo_puede_tomar_visita(vehiculo, visita, peso_total, tiempo_total, False):
                        if despacho is None:
                            despacho = RutDespacho.objects.create(
                                fecha=timezone.now(),
                                vehiculo=vehiculo,
                                peso=visita.peso,
                                volumen=visita.volumen,
                                tiempo=visita.tiempo,
                                tiempo_servicio=visita.tiempo_servicio,
                                tiempo_trayecto=visita.tiempo_trayecto,
                                visitas=1
                            )
                            vehiculo.estado_asignado = True
                            vehiculo.save()
                            despachos_creados += 1
                        else:
                            despacho.peso += visita.peso
                            despacho.volumen += visita.volumen
                            despacho.tiempo = (Decimal(despacho.tiempo) + Decimal(visita.tiempo)).quantize(
                                decimal_6_places,
                                rounding=ROUND_HALF_UP
                            )
                            despacho.tiempo_servicio = (Decimal(despacho.tiempo_servicio) + Decimal(visita.tiempo_servicio)).quantize(
                                decimal_6_places,
                                rounding=ROUND_HALF_UP
                            )
                            despacho.tiempo_trayecto = (Decimal(despacho.tiempo_trayecto) + Decimal(visita.tiempo_trayecto)).quantize(
                                decimal_6_places,
                                rounding=ROUND_HALF_UP
                            )
                            despacho.visitas += 1
                            despacho.save()

                        peso_total += visita.peso
                        tiempo_total += visita.tiempo
                        
                        visita.estado_despacho = True
                        visita.despacho = despacho
                        visita.save()
                        
                        visitas_pendientes.remove(visita)
                        visitas_asignadas_este_vehiculo += 1

                vehiculo_index += 1

            mensaje = (
                f"Operación completada: {despachos_creados} rutas creadas"
                + (f"Pendientes: {len(visitas_pendientes)} visitas (IDs: {', '.join(str(v.id) for v in visitas_pendientes)})" 
                if visitas_pendientes else "")
            )

            return Response({
                'mensaje': mensaje,
                'status': status.HTTP_200_OK
            })
        
    @action(detail=False, methods=["post"], url_path=r'ubicar',)
    def ubicar(self, request):             
        raw = request.data
        cantidad = 0
        franjas = RutFranja.objects.all()
        visitas = RutVisita.objects.filter(estado_despacho = False, estado_decodificado = True)
        for visita in visitas:
            respuesta = ubicar_punto(franjas, visita.latitud, visita.longitud)
            if respuesta['encontrado']:
                visita.franja_id = respuesta['franja']['id']
                visita.franja_codigo = respuesta['franja']['codigo']
                visita.estado_franja = True
            else:
                visita.franja_id = None
                visita.franja_codigo = None
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
        raw = request.data
        filtros = raw.get('filtros')
        visitas = RutVisita.objects.filter(estado_despacho=False, estado_devolucion=False)
        errores = RutVisita.objects.filter(estado_decodificado=False, estado_despacho= False)
        alertas = RutVisita.objects.filter(estado_decodificado_alerta=True, estado_despacho= False)
        if filtros:
            for filtro in filtros:                    
                operador = filtro.get('operador', None)
                if operador == 'range':
                    visitas = visitas.filter(**{filtro['propiedad']+'__'+operador: (filtro['valor1'], filtro['valor2'])})
                    errores = errores.filter(**{filtro['propiedad']+'__'+operador: (filtro['valor1'], filtro['valor2'])})
                    alertas = alertas.filter(**{filtro['propiedad']+'__'+operador: (filtro['valor1'], filtro['valor2'])})
                else:
                    visitas = visitas.filter(**{filtro['propiedad']+'__'+operador: filtro['valor1']})
                    errores = errores.filter(**{filtro['propiedad']+'__'+operador: filtro['valor1']})
                    alertas = alertas.filter(**{filtro['propiedad']+'__'+operador: filtro['valor1']})


        visitas = visitas.aggregate(
            cantidad=Count('id'), 
            peso=Coalesce(Sum('peso'), 0.0),
            tiempo=Coalesce(Sum('tiempo'), Decimal(0.0)),
            tiempo_servicio=Coalesce(Sum('tiempo_servicio'), Decimal(0.0)),
            tiempo_trayecto=Coalesce(Sum('tiempo_trayecto'), Decimal(0.0))
            
        )    
        errores = errores.aggregate(
            cantidad=Count('id'))        
        alertas = alertas.aggregate(
            cantidad=Count('id'))        
        return Response({'resumen': visitas, 'errores': errores, 'alertas':alertas}, status=status.HTTP_200_OK)   

    @action(detail=False, methods=["post"], url_path=r'resumen-pendiente',)
    def resumen_pendiente(self, request):
        raw = request.data
        filtros = raw.get('filtros')
        visitas = RutVisita.objects.all()
        if filtros:
            for filtro in filtros:
                visitas = visitas.filter(**{filtro['propiedad']: filtro['valor1']})
        visitas = visitas.values('franja_codigo').annotate(
            cantidad=Count('id'), 
            peso=Coalesce(Sum('peso'), 0.0),
            tiempo=Coalesce(Sum('tiempo'), Decimal(0.0)),
            tiempo_servicio=Coalesce(Sum('tiempo_servicio'), Decimal(0.0)),
            tiempo_trayecto=Coalesce(Sum('tiempo_trayecto'), Decimal(0.0)),
            )    
        return Response({'resumen': visitas}, status=status.HTTP_200_OK) 

    @action(detail=False, methods=["post"], url_path=r'seleccionar-direccion-alternativa',)
    def seleccionar_direccion_alternativa(self, request):             
        raw = request.data
        id = raw.get('id')
        latitud = raw.get('latitud')
        longitud = raw.get('longitud')
        destinatario_direccion_formato = raw.get('destinatario_direccion_formato')
        if id and latitud and longitud and destinatario_direccion_formato:
            try:                
                visita = RutVisita.objects.get(pk=id)
                franjas = RutFranja.objects.all()
                respuesta = ubicar_punto(franjas, latitud, longitud)
                if respuesta['encontrado']:                    
                    visita.franja_id = respuesta['franja']['id']
                    visita.estado_franja = True
                else:
                    visita.franja_id = None
                    visita.estado_franja = False 
                visita.latitud = latitud
                visita.longitud = longitud
                visita.destinatario_direccion_formato = destinatario_direccion_formato
                visita.estado_decodificado_alerta = False
                visita.save()               
                return Response({'mensaje': 'Se actualizo la visita'}, status=status.HTTP_200_OK)
            except RutVisita.DoesNotExist:
                return Response({'mensaje':'La visita no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
        
    @action(detail=False, methods=["post"], url_path=r'actualizar-direccion',)
    def actualizar_direccion(self, request):             
        raw = request.data
        id = raw.get('id')
        destinatario_direccion = raw.get('destinatario_direccion')
        numero = raw.get('numero')
        documento = raw.get('documento')
        destinatario = raw.get('destinatario')
        destinatario_telefono = raw.get('destinatario_telefono')
        peso = raw.get('peso')
        volumen = raw.get('volumen')
        if id and destinatario and destinatario_direccion:
            try:  
                google = Google()              
                visita = RutVisita.objects.get(pk=id)                                 
                destinatario_direccion = destinatario_direccion.replace("\t", "").replace("\n", "")
                destinatario_direccion = re.sub(r'[\s\u2000-\u200F\u3000\u31A0]+', ' ', destinatario_direccion).strip()   
                destinatario_direccion = re.sub(r'[\s\u2000-\u200F\u3000\u3164]+', ' ', destinatario_direccion).strip()                 
                destinatario_direccion = re.sub(r'\s+', ' ', destinatario_direccion.strip())                    
                destinatario_direccion = destinatario_direccion[:150]
                if visita.destinatario_direccion != destinatario_direccion:
                    visita.destinatario_direccion = destinatario_direccion
                    visita.estado_decodificado = False
                    visita.estado_decodificado_alerta = False
                    if destinatario_direccion:                   
                        direccion = CtnDireccion.objects.filter(direccion=destinatario_direccion).first()
                        if direccion:
                            visita.estado_decodificado = True            
                            visita.latitud = direccion.latitud                        
                            visita.longitud = direccion.longitud
                            visita.destinatario_direccion_formato = direccion.direccion_formato
                            visita.resultados = direccion.resultados
                            if direccion.cantidad_resultados > 1:
                                visita.estado_decodificado_alerta = True                                
                        else:
                            respuesta = google.decodificar_direccion(destinatario_direccion)
                            if respuesta['error'] == False:   
                                visita.estado_decodificado = True            
                                visita.latitud = respuesta['latitud']
                                visita.longitud = respuesta['longitud']
                                visita.destinatario_direccion_formato = respuesta['direccion_formato']
                                visita.resultados = respuesta['resultados']
                                if respuesta['cantidad_resultados'] > 1:
                                    visita.estado_decodificado_alerta = True                
                    if visita.estado_decodificado == True:
                        franjas = RutFranja.objects.all()
                        respuesta = ubicar_punto(franjas, visita.latitud, visita.longitud)
                        if respuesta['encontrado']:
                            visita.franja_id = respuesta['franja']['id']
                            visita.estado_franja = True
                        else:
                            visita.franja_id = None
                            visita.estado_franja = False                                                     
                visita.numero = numero
                visita.documento = documento
                visita.destinatario = destinatario
                visita.destinatario_telefono = destinatario_telefono
                visita.peso = peso
                visita.volumen = volumen
                visita.save()               
                return Response({'mensaje': 'Se actualizo la visita'}, status=status.HTTP_200_OK)
            except RutVisita.DoesNotExist:
                return Response({'mensaje':'La visita no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    

    @action(detail=False, methods=["post"], url_path=r'despacho-retirar',)
    def despacho_retirar(self, request):             
        raw = request.data
        id = raw.get('id')
        if id:
            try:                               
                visita = RutVisita.objects.get(pk=id) 
                despacho = RutDespacho.objects.get(pk=visita.despacho_id)
                if despacho.estado_aprobado == True:
                    return Response({'mensaje': 'No se puede retirar la visita porque el despacho esta aprobado.'}, status=status.HTTP_400_BAD_REQUEST)        
                else:
                    despacho.peso = despacho.peso - visita.peso
                    despacho.volumen = despacho.volumen - visita.volumen
                    despacho.visitas -= 1
                    despacho.save()                 
                    visita.despacho = None
                    visita.estado_despacho = False
                    visita.save()               
                    return Response({'mensaje': 'Se retiro la visita del despacho'}, status=status.HTTP_200_OK)
            except RutVisita.DoesNotExist:
                return Response({'mensaje':'La visita no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)     

    @action(detail=False, methods=["post"], url_path=r'despacho-cambiar',)
    def despacho_cambiar(self, request):             
        raw = request.data
        id = raw.get('id')
        despacho_id = raw.get('despacho_id')
        if id and despacho_id:            
            try:                               
                visita = RutVisita.objects.get(pk=id) 
                if visita.despacho_id != despacho_id:               
                    try:
                        despacho_nuevo = RutDespacho.objects.get(pk=despacho_id)
                        if visita.despacho_id:                                                
                            despacho_actual = RutDespacho.objects.get(pk=visita.despacho_id)
                            despacho_actual.peso = despacho_actual.peso - visita.peso
                            despacho_actual.volumen = despacho_actual.volumen - visita.volumen
                            despacho_actual.visitas -= 1
                            despacho_actual.save()

                            despacho_nuevo.peso = despacho_nuevo.peso + visita.peso
                            despacho_nuevo.volumen = despacho_nuevo.volumen + visita.volumen
                            despacho_nuevo.visitas += 1
                            despacho_nuevo.save()

                            visita.despacho = despacho_nuevo
                            visita.save() 
                            return Response({'mensaje': 'Se cambio la visita de despacho'}, status=status.HTTP_200_OK)                        
                        else:
                            return Response({'mensaje':'La visita no tiene despacho', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                                                                            
                    except RutDespacho.DoesNotExist:
                        return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                
                else:
                    return Response({'mensaje':'La visita ya está en este despacho', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                
            except RutVisita.DoesNotExist:
                return Response({'mensaje':'La visita no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'entrega',)
    def entrega(self, request):                     
        id = request.POST.get('id')
        imagenes = request.FILES.getlist('imagenes')
        firmas = request.FILES.getlist('firmas')
        fecha_entrega_texto = request.POST.get('fecha_entrega')
        datos_adicionales = request.POST.get('datos_adicionales')        
        if id and fecha_entrega_texto:
            try:
                fecha_entrega_naive = datetime.strptime(fecha_entrega_texto, '%Y-%m-%d %H:%M')
                fecha_entrega = timezone.make_aware(fecha_entrega_naive)
                if fecha_entrega > timezone.now():
                    return Response({'mensaje':'La fecha de entrega no puede ser mayor a la fecha actual', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                             
            except ValueError:
                return Response({'mensaje':'Formato de fecha inválido. Use YYYY-MM-DD HH:MM', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
            try:
                visita = RutVisita.objects.get(pk=id)                            
            except RutVisita.DoesNotExist:
                return Response({'mensaje':'La visita no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)           
            if visita.estado_entregado == False:  
                if visita.despacho_id:
                    try:
                        despacho = RutDespacho.objects.get(pk=visita.despacho_id)
                    except ValueError:
                        return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST) 
                    with transaction.atomic():          
                        configuracion = GenConfiguracion.objects.filter(pk=1).values('rut_sincronizar_complemento')[0]                                               
                        datos_entrega = json_texto(datos_adicionales)
                        visita.estado_entregado = True
                        visita.fecha_entrega = fecha_entrega
                        visita.datos_entrega = datos_entrega
                        visita.save()
                        despacho.visitas_entregadas += 1
                        despacho.save()                                    
                        backblaze = Backblaze()
                        tenant = request.tenant.schema_name                    
                        if imagenes:                        
                            for imagen in imagenes:       
                                #file_content = imagen.read()                                  
                                file_content = Imagen.comprimir_imagen_jpg(imagen, calidad=20, max_width=1920)
                                nombre_archivo = f'{id}.jpg'                                                   
                                id_almacenamiento, tamano, tipo, uuid, url = backblaze.subir_data(file_content, tenant, nombre_archivo)
                                archivo = GenArchivo()
                                archivo.archivo_tipo_id = 2
                                archivo.almacenamiento_id = id_almacenamiento
                                archivo.nombre = nombre_archivo
                                archivo.tipo = tipo
                                archivo.tamano = tamano
                                archivo.uuid = uuid
                                archivo.codigo = id
                                archivo.modelo = "RutVisita"
                                archivo.url = url
                                archivo.save()
                        if firmas:
                            for firma in firmas:       
                                #file_content = firma.read()   
                                file_content = Imagen.comprimir_imagen_jpg(firma, calidad=20, max_width=1920)                                                         
                                nombre_archivo = f'{id}.png'                                                   
                                id_almacenamiento, tamano, tipo, uuid, url = backblaze.subir_data(file_content, tenant, nombre_archivo)
                                archivo = GenArchivo()
                                archivo.archivo_tipo_id = 3
                                archivo.almacenamiento_id = id_almacenamiento
                                archivo.nombre = nombre_archivo
                                archivo.tipo = tipo
                                archivo.tamano = tamano
                                archivo.uuid = uuid
                                archivo.codigo = id
                                archivo.modelo = "RutVisita"
                                archivo.url = url
                                archivo.save()                        
                        if configuracion['rut_sincronizar_complemento']:
                            imagenes_b64 = []
                            if imagenes:                        
                                for imagen in imagenes:       
                                    file_content = imagen.read()   
                                    base64_encoded = base64.b64encode(file_content).decode('utf-8')                                                    
                                    imagenes_b64.append({
                                        'base64': base64_encoded,
                                    })     
                            firmas_b64 = []
                            if firmas:
                                for firma in firmas:       
                                    file_content = firma.read()   
                                    base64_encoded = base64.b64encode(file_content).decode('utf-8')                                                    
                                    firmas_b64.append({
                                        'base64': base64_encoded,
                                    })                                                                                                                                                                                                     
                            self.entrega_complemento(visita, imagenes_b64, firmas_b64, datos_entrega)
                        return Response({'mensaje': f'Entrega con exito'}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'La visita no tiene despacho', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)  
                
            else:
                return Response({'mensaje':'La visita ya fue entregada con anterioridad', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'consulta-documento',)
    def consulta_documento(self, request):             
        raw = request.data
        despacho_id = raw.get('despacho_id')    
        estado_despacho = raw.get('estado_despacho', None)
        numero = raw.get('numero')
        if numero:
            visita = RutVisita.objects.filter(numero=numero)   
            if despacho_id:
                visita = visita.filter(despacho_id=despacho_id)  
            if estado_despacho == True:  
                visita = visita.filter(estado_despacho=True)
            if estado_despacho == False:  
                visita = visita.filter(estado_despacho=False)
            visita = visita.first()
            if visita:
                return Response({'id': visita.id}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':f'La visita con numero {numero} no existe', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                                                              
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    

    @action(detail=False, methods=["post"], url_path=r'liberar',)
    def liberar(self, request):             
        raw = request.data
        id = raw.get('id')        
        if id:
            try:
                visita = RutVisita.objects.get(pk=id)                            
            except RutVisita.DoesNotExist:
                return Response({'mensaje':'La visita no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)            
            if visita.estado_entregado == False and visita.estado_despacho == True:                
                despacho = RutDespacho.objects.get(pk=visita.despacho_id)                
                despacho.visitas_liberadas += 1
                despacho.peso = despacho.peso - visita.peso
                despacho.volumen = despacho.volumen - visita.volumen
                despacho.tiempo = despacho.tiempo - visita.tiempo
                despacho.tiempo_servicio = despacho.tiempo_servicio - visita.tiempo_servicio
                despacho.tiempo_trayecto = despacho.tiempo_trayecto - visita.tiempo_trayecto
                despacho.visitas = despacho.visitas - 1    
                if visita.estado_novedad:
                    despacho.visitas_novedad = despacho.visitas_novedad - 1              
                despacho.save()  
                visita.estado_despacho = False 
                visita.despacho = None           
                visita.save()                        
                return Response({'mensaje': f'Se libero con exito'}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':'La visita ya fue entregada o no esta despachada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)        
            
    @action(detail=False, methods=["post"], url_path=r'entrega-complemento',)
    def entrega_complemento_action(self, request):   
        backblaze = Backblaze()
        visitas = RutVisita.objects.filter(estado_entregado=True, estado_entregado_complemento=False)                
        for visita in visitas:
            imagenes_b64 = []
            archivos = GenArchivo.objects.filter(modelo='RutVisita', codigo=visita.id, archivo_tipo_id=2)
            for archivo in archivos:
                contenido = backblaze.descargar_bytes(archivo.almacenamiento_id)
                if contenido is not None:
                    contenido_base64 = base64.b64encode(contenido).decode('utf-8')                    
                    imagenes_b64.append({
                        'base64': contenido_base64,
                    })   
            firmas_b64 = []
            archivos = GenArchivo.objects.filter(modelo='RutVisita', codigo=visita.id, archivo_tipo_id=3)
            for archivo in archivos:
                contenido = backblaze.descargar_bytes(archivo.almacenamiento_id)
                if contenido is not None:
                    contenido_base64 = base64.b64encode(contenido).decode('utf-8')                    
                    firmas_b64.append({
                        'base64': contenido_base64,
                    })                              
            self.entrega_complemento(visita, imagenes_b64, firmas_b64, visita.datos_entrega)
        return Response({'mensaje': f'Entrega complemento {visitas.count()}'}, status=status.HTTP_200_OK)

    def limpiar_direccion(self, direccion):
        if not direccion:
            direccion = ""
        direccion = direccion.replace("\t", "").replace("\n", "")
        direccion = re.sub(r'[\s\u2000-\u200F\u3000\u31A0]+', ' ', direccion).strip()   
        direccion = re.sub(r'[\s\u2000-\u200F\u3000\u3164]+', ' ', direccion).strip()                 
        direccion = re.sub(r'\s+', ' ', direccion.strip())                    
        direccion = direccion[:150]        
        return direccion
    
    def entrega_complemento(self, visita: RutVisita, imagenes_b64, firmas_b64, datos_entrega):
        holmio = Holmio()
        fecha_formateada = visita.fecha_entrega.strftime('%Y-%m-%d %H:%M')
        parametros = {
            'codigoGuia': visita.numero,
            'fechaEntrega': fecha_formateada,
            'usuario': 'ruteo'
        }
        if imagenes_b64:
            parametros['imagenes'] = imagenes_b64
        if firmas_b64:
            parametros['firmarBase64'] = firmas_b64[0]
        if datos_entrega:
            parametros.update(datos_entrega)                    
        respuesta = holmio.entrega(parametros)
        visita.estado_entregado_complemento = True
        visita.save()
        return True