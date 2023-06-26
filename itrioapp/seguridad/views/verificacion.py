from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from seguridad.serializers import UserSerializer, UserListSerializer, UserDetalleSerializer, CustomTokenObtainPairSerializer, CustomUserSerializer, VerificacionSerializer
from django.shortcuts import get_object_or_404
from seguridad.models import User, Verificacion
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from decouple import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import secrets

class VerificacionNuevo(APIView):
    def post(self, request, *args, **kwargs):   
        verificacion_data = request.data    
        token = secrets.token_urlsafe(20)
        verificacion_data["token"] = token
        verificacion_data["vence"] = datetime.now().date() + timedelta(days=1)
        verificacion_serializer = VerificacionSerializer(data = verificacion_data)        
        usuario = User.objects.get(username = verificacion_data.get('username'))
        if usuario:
            verificacion_data["codigo_usuario_fk"] = usuario.id
            if verificacion_serializer.is_valid():                                             
                verificacion_serializer.save()
                if verificacion_data.get('accion') == 'registro':
                    message = Mail(
                        from_email='tisemantica@gmail.com',
                        to_emails=usuario.email,
                        subject='Debe verificar su cuenta',
                        html_content='Enlace para verificar http://muup.online/auth/verificacion/' + token)
                    sg = SendGridAPIClient(config('KEY_SENDGRID'))
                    sg.send(message)    
                if verificacion_data.get('accion') == 'clave':
                    message = Mail(
                        from_email='tisemantica@gmail.com',
                        to_emails=usuario.email,
                        subject='Cambio de clave',
                        html_content='Enlace para cambiar la clave http://muup.online/clave/cambiar/' + token)
                    sg = SendGridAPIClient(config('KEY_SENDGRID'))
                    sg.send(message) 
                return Response({'verificacion': verificacion_data}, status=status.HTTP_201_CREATED)            
            return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':3, 'validaciones': verificacion_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje':'El usuario para recuperar la clave no existe', 'codigo':8, 'validaciones': verificacion_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class VerificacionToken(APIView):

    def post(self, request):
        tokenUrl = request.data.get('token')
        verificacion = Verificacion.objects.filter(token=tokenUrl).first()
        if verificacion:
            if verificacion.estado_usado == False:
                fechaActual = datetime.now().date()
                if fechaActual <= verificacion.vence:
                    verificacion.estado_usado = True
                    verificacion.save()
                    usuario = User.objects.get(id = verificacion.codigo_usuario_fk)
                    usuario.is_active = True
                    usuario.save()
                    verificacionSerializer = VerificacionSerializer(verificacion)                
                    return Response({'verificado': True, 'verificacion': verificacionSerializer.data}, status=status.HTTP_200_OK)
                return Response({'mensaje':'El token de la verificacion esta vencido', 'codigo': 6, 'codigoUsuario': verificacion.codigo_usuario_fk}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'mensaje':'La verificacion ya fue usada', 'codigo': 5, 'codigoUsuario': verificacion.codigo_usuario_fk}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje':'No se ha encontrado la verificacion', 'codigo': 4}, status=status.HTTP_400_BAD_REQUEST)
