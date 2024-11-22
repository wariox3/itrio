from contenedor.models import CtnDireccion
from ruteo.models.visita import RutVisita
from decouple import config
from django.utils.timezone import now
import requests
import googlemaps

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
                location = data['results'][0]['geometry']['location']
                direccion_formato = data['results'][0]['formatted_address']
                direccion = CtnDireccion()
                direccion.fecha = now()
                direccion.direccion = direccion_parametro
                direccion.direccion_formato = direccion_formato
                direccion.latitud = location['lat']
                direccion.longitud = location['lng']
                direccion.save()
                return {
                    "error": False,
                    "direccion_formato": direccion_formato,
                    "latitud": location['lat'],
                    "longitud": location['lng']
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
      