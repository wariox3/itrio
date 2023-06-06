from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from decouple import config 

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
        prueba = config('KEY_SENDGRID')
        return Response("Hola mundo" + prueba)

