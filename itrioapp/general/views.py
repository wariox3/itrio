from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Contacto, Item
from general.serializers import ContactoSerializer, ItemSerializer
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

# Basados en ModelViewSet
class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer    
    permission_classes = [permissions.IsAuthenticated]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

