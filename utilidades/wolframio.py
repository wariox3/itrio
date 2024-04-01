import requests
import json


def consumirPost(data, url):
    url = "http://159.203.18.130/wolframio/public/index.php" + url

    json_data = json.dumps(data)

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json_data, headers=headers)

    # Obtener la respuesta como JSON
    resp = response.json()

    return resp


