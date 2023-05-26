from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from users.serializers import UserSerializer, UserListSerializer, UserDetalleSerializer, CustomTokenObtainPairSerializer, CustomUserSerializer, VerificacionSerializer
from django.shortcuts import get_object_or_404
from users.models import User, Verificacion
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from datetime import datetime, timedelta, date
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
            user_serializer.save()
            #Enviar verificacion (metodo)
            ultimo_registro = User.objects.filter(username=request.data.get('username'))
            for user in ultimo_registro:
                request.data['codigo_usuario_fk'] = user.id
                verificacionAPIView = VerificacionAPIView()
                verificacionAPIView.post(request)
            return Response({'message':'Usuario registrado', 'user': 'usuario'}, status=status.HTTP_201_CREATED)
        return Response({'message:':'Errores en el registro', 'errors': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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

class VerificacionAPIView(APIView):

    def get(self, request):
        verificaciones = Verificacion.objects.all()
        verificaciones_serializer = VerificacionSerializer(verificaciones, many = True)  
        return Response(verificaciones_serializer.data)
    
    def post(self, request, *args, **kwargs):   
        verificacion_data = request.data
        token = secrets.token_urlsafe(20)
        verificacion_data["token"] = token
        verificacion_data["vence"] = datetime.now().date() + timedelta(days=1)
        verificacion_serializer = VerificacionSerializer(data = verificacion_data)        
        if verificacion_serializer.is_valid(): 
            verificacion_serializer.save()
            mensaje = "La url es: www.prueba.com/verificar/" + token    
            send_mail(
                "Asunto del mensaje",
                mensaje,
                "from@example.com",
                ["to@example.com"],
                fail_silently=False,
            )    
            return Response({'message':'Verificacion creada'}, status=status.HTTP_201_CREATED)
        return Response({'message:':'Errores en el registro', 'errors': verificacion_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class VerificacionTokenAPIView(APIView):

    def post(self, request):
        tokenUrl = request.data.get('token')
        try:
            usuarioVerificacion = Verificacion.objects.get(token=tokenUrl)
            if(usuarioVerificacion):
                if(usuarioVerificacion.estado_usado == False):
                    fechaActual = datetime.now().date()
                    if(fechaActual < usuarioVerificacion.vence):
                        usuarioVerificacion.estado_usado = True
                        usuarioVerificacion.save()
                        return Response({'message': "Token validado con exitosamente"}, status=status.HTTP_200_OK)
                    return Response({'message':'Errores con el token', 'errors': "Token ya se encuentra vencido por favor generar uno nuevo" }, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message':'Errores con el token', 'errors': "Token ya se encuentra en uso" }, status=status.HTTP_400_BAD_REQUEST)
        except Verificacion.DoesNotExist:
            return Response({'message':'Errores con el token',  'errors':'No existe el token'}, status=status.HTTP_400_BAD_REQUEST)
