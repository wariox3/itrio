from contenedor.models import CtnDireccion
from ruteo.models.visita import RutVisita
from decouple import config
from django.utils.timezone import now
import requests
import googlemaps
from general.models.configuracion import GenConfiguracion

class Google():

    def __init__(self):
        api_key = config('GOOGLE_MAPS_API_KEY')
        self.gmaps = googlemaps.Client(key=api_key)

    def decodificar_direccion(self, direccion_parametro):                                
        api_key = config('GOOGLE_MAPS_API_KEY')
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            #"address": f"{direccion_parametro}, COLOMBIA",
            "address": direccion_parametro,
            "key": api_key,
            "components": "country:CO"
        }
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':                
                resultados = data['results']
                cantidad_resultados = len(resultados)
                location = resultados[0]['geometry']['location']
                direccion_formato = resultados[0]['formatted_address']
                direccion = CtnDireccion()
                direccion.fecha = now()
                direccion.direccion = direccion_parametro
                direccion.direccion_formato = direccion_formato
                direccion.latitud = location['lat']
                direccion.longitud = location['lng']
                direccion.cantidad_resultados = cantidad_resultados
                direccion.resultados = resultados
                direccion.save()
                return {
                    "error": False,
                    "direccion_formato": direccion_formato,
                    "latitud": location['lat'],
                    "longitud": location['lng'],
                    "cantidad_resultados": cantidad_resultados,
                    "resultados": resultados
                }
            else:
                return {"error": True, "mensaje": data.get('error_message', 'Error desconocido de google')}
        else:
            return {"error": True, "mensaje": "Estatus code de google diferente a 200"}

    def calcular_ruta(self, visitas):      
                                      
        api_key = config('GOOGLE_MAPS_API_KEY')
        base_url = "https://maps.googleapis.com/maps/api/directions/json"
        waypoints = "|".join([f"{visita['latitud']},{visita['longitud']}" for visita in visitas])        
        cantidad_visitas = len(visitas)
        params = {
            "origin": f"6.197023,-75.585760",
            "destination": f"6.197023,-75.585760",
            "waypoints": f"optimize:true|{waypoints}",
            "key": api_key
        }
        response = requests.get(base_url, params=params)                
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':                                
                ruta = data["routes"][0]                
                waypoint_order = ruta["waypoint_order"]
                entregas_ordenadas = [visitas[i] for i in waypoint_order]
                
                '''for i, leg in enumerate(ruta["legs"]):
                    visita_actual = entregas_ordenadas[i]
                    distancia = leg["distance"]["value"]  # En metros
                    tiempo = leg["duration"]["value"]  # En segundos

                    visita_actualizar = RutVisita.objects.get(id=visita_actual["id"])
                    visita_actualizar.orden = i + 1
                    #visita_actualizar.distancia_proxima = distancia
                    #visita_actualizar.tiempo_proxima = tiempo
                    visita_actualizar.save()'''

                return {
                    "error": False,
                    "ruta": ruta, 
                    "ruta_puntos": ruta["overview_polyline"]["points"],
                    "orden_entregas": entregas_ordenadas,
                }
            else:
                return {"error": True, "mensaje": data.get('error_message', 'Error desconocido de google')}
        else:
            return {"error": True, "mensaje": "Estatus code de google diferente a 200"}
    
    def direcciones(self, visitas):
        configuracion = GenConfiguracion.objects.first()
        origen_lat = configuracion.rut_latitud
        origen_lng = configuracion.rut_longitud
        
        total_visitas = len(visitas)
        
        if total_visitas > 25:
            visitas = visitas[:25]
            advertencia = f"Se han limitado las {total_visitas} visitas a las últimas 25 para la API"
        else:
            advertencia = None
        
        if not visitas:
            return {"error": True, "mensaje": "No hay visitas para calcular la ruta"}
        
        ultimo_waypoint = visitas[-1]
        destino_lat = ultimo_waypoint['latitud']
        destino_lng = ultimo_waypoint['longitud']
        
        waypoints_restantes = visitas[:-1]
        waypoints_str = "|".join([f"{visita['latitud']},{visita['longitud']}" for visita in waypoints_restantes])
        
        api_key = config('GOOGLE_MAPS_API_KEY')
        base_url = "https://maps.googleapis.com/maps/api/directions/json"
        
        params = {
            "origin": f"{origen_lat},{origen_lng}",
            "destination": f"{destino_lat},{destino_lng}",
            "waypoints": f"optimize:false|{waypoints_str}" if waypoints_str else "",
            "key": api_key
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                ruta = data["routes"][0]
                resultado = {
                    "error": False,
                    "response": response,
                    "data": data,
                    "ruta": ruta,
                    "ruta_puntos": ruta["overview_polyline"]["points"]
                }
                if advertencia:
                    resultado["advertencia"] = advertencia
                return resultado
            else:
                return {"error": True, "mensaje": data.get('error_message', 'Error desconocido de Google')}
        else:
            return {"error": True, "mensaje": "Estatus code de Google diferente a 200"}

    def matriz_distancia(self, visitas_ubicaciones):
        api_key = config('GOOGLE_MAPS_API_KEY')                                                        
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": '|'.join(f"{lat},{lng}" for lat, lng in visitas_ubicaciones),
            "destinations": '|'.join(f"{lat},{lng}" for lat, lng in visitas_ubicaciones),
            "mode": "driving",
            "key": api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()        
            if data['status'] == 'OK':  
                distances = [
                    [element['distance']['value'] for element in row['elements']]
                    for row in data['rows']
                ]                   
                durations = [
                    [element['duration']['value'] for element in row['elements']]
                    for row in data['rows']
                ]
                return {'error':False, 'distancias':distances, 'duraciones': durations}                                 
            else:
               return {"error": True, "mensaje": data.get('error_message', 'Error desconocido de google')}
        else:
           return {"error": True, "mensaje": "Estatus code de google diferente a 200"}  
      