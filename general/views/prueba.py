from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from decouple import config 
from utilidades.space_do import SpaceDo
from general.models.item import Item
import random

def vistaTamplate(request):
    return render(request, "general/prueba.html")

def vista(request):
    send_mail(
        "Subject here",
        "Here is the message.",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )
    return HttpResponse("Hola mundo")

class PruebaView(APIView):
    def get(self, request):
        for i in range(1, 15550):
            item = Item(
                codigo=i,
                referencia=f"REF {i}",
                nombre=f"Producto {i}",
                costo=random.randrange(100000, 500000),
                precio=random.randrange(500000, 1000000)
                )
            item.save()
        prueba = config('KEY_SENDGRID')
        return Response("Hola mundo" + prueba)

