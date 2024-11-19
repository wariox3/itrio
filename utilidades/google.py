from contenedor.models import CtnDireccion
import requests
from decouple import config
from django.utils.timezone import now

class Google():

    def __init__(self):
        pass

    def decodificar_direccion(self, direccion_parametro):                                
        api_key = config('GOOGLE_MAPS_API_KEY')
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": direccion_parametro,
            "key": api_key
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
                ruta_optima = data["routes"][0]                
                orden_optimo = ruta_optima["waypoint_order"]
                entregas_ordenadas = []
                tiempo_entre_visitas = []

                for i, orden in enumerate(orden_optimo):
                    visita_actual = visitas[orden]
                    visita_actual["orden"] = i + 1

                    if i > 0:
                        tiempo = ruta_optima["legs"][i - 1]["duration"]["value"]  # Tiempo en segundos
                        visita_actual["tiempo_desde_anterior"] = tiempo
                        tiempo_entre_visitas.append(tiempo)
                    else:
                        visita_actual["tiempo_desde_anterior"] = 0  # Primera visita no tiene tiempo anterior

                    entregas_ordenadas.append(visita_actual)
                return {
                    "error": False,
                    "ruta": ruta_optima["overview_polyline"]["points"],
                    "orden_entregas": entregas_ordenadas,
                    "distancia_total": sum(leg["distance"]["value"] for leg in ruta_optima["legs"]),
                    "tiempo_total": sum(leg["duration"]["value"] for leg in ruta_optima["legs"]),
                    "tiempo_entre_visitas": tiempo_entre_visitas
                }
            else:
                return {"error": True, "mensaje": data.get('error_message', 'Error desconocido de google')}
        else:
            return {"error": True, "mensaje": "Estatus code de google diferente a 200"}