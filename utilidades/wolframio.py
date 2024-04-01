import requests
import json


def consumirPost(data, url):
    url = "http://159.203.18.130/wolframio/public/index.php" + url

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, data=json_data, headers=headers)
        response.raise_for_status()  # Verificar el estado de la respuesta

        # Obtener la respuesta como JSON
        resp = response.json()

    except requests.exceptions.HTTPError as e:
        # Si hay un error HTTP (por ejemplo, código 400)
        resp = {"mensaje": str(e.response.text)}

    except Exception as e:
        # Manejar otros tipos de excepciones
        print("Error:", e)
        resp = {"error": str(e)}

    return resp


