from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from general.models.item import Item
from utilidades.correo import Correo
from decouple import config 
import random

@api_view(['GET'])
def enviar_coreo(request):
    correo = Correo() 
    contenido='Hola mundo!'
    correo.enviar('maestradaz3@gmail.com', 'Correo de prueba', contenido) 
    return Response({"message": "Hello, world!"})

class PruebaView(APIView):
    def get(self, request):
        prueba = config('KEY_SENDGRID')
        return Response("Hola mundo" + prueba)

