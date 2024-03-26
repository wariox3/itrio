from django.http import JsonResponse
from general.models.respuesta_electronica import RespuestaElectronica
from django.utils import timezone
import requests
import json


def consumirPost(data, url):
    url = "http://159.203.18.130/wolframio/public/index.php" + url

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, data=json_data, headers=headers)

        # Verificar el estado de la respuesta
        response.raise_for_status()

        # Obtener la respuesta como JSON
        resp = response.json()

    except requests.exceptions.HTTPError as err:
        # Manejar el error HTTP
        print(f"Error HTTP: {err}")

    except Exception as err:
        # Manejar cualquier otra excepción
        print(f"Error inesperado: {err}")

    return resp


