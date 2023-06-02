from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from users.serializers import UserSerializer, UserListSerializer, UserDetalleSerializer, CustomTokenObtainPairSerializer, CustomUserSerializer, VerificacionSerializer
from django.shortcuts import get_object_or_404
from users.models import User, Verificacion
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from decouple import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import secrets

class UsuarioViewSet(GenericViewSet):
    model = User
    queryset = None
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    detalle_serializer_class = UserDetalleSerializer
    
    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)
    
    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.serializer_class.Meta.model.objects.all().values('id', 'username', 'email', 'codigo_cliente_fk', 'dominio')
        return self.queryset

    def list(self, request):
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            #Enviar verificacion (metodo)
            request.data['username'] = user.username
            request.data['accion'] = 'registro'
            verificacionAPIView = VerificacionNuevo()
            verificacionAPIView.post(request)
            return Response({'usuario': user_serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'mensaje':'Errores en el registro del usuario', 'codigo':2, 'validaciones': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.detalle_serializer_class(user)
        return Response(user_serializer.data)
    
class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh-token': login_serializer.validated_data.get('refresh'),
                    'user':user_serializer.data
                }, status=status.HTTP_200_OK)
            return Response({'error':'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)        

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
                        html_content='Enlace para verificar http://muup.online/varificacion/' + token)
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

class ClaveCambiar(APIView):

    def post(self, request):    
        codigoUsuario = request.data.get('id')
        clave = request.data.get('password')
        usuario = User.objects.get(id = codigoUsuario)
        usuario.set_password(clave)
        usuario.save()
        return Response({'cambio': True}, status=status.HTTP_200_OK)
