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
            user = user_serializer.save()
            #Enviar verificacion (metodo)
            request.data['codigo_usuario_fk'] = user.id
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
            return Response({'verificacion': verificacion_data}, status=status.HTTP_201_CREATED)
        return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':3, 'validaciones': verificacion_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
                    return Response({'verificacion': True}, status=status.HTTP_200_OK)
                return Response({'mensaje':'El token de la verificacion esta vencido', 'codigo': 6, 'codigoUsuario': verificacion.codigo_usuario_fk}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'mensaje':'La verificacion ya fue usada', 'codigo': 5, 'codigoUsuario': verificacion.codigo_usuario_fk}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje':'No se ha encontrado la verificacion', 'codigo': 4}, status=status.HTTP_400_BAD_REQUEST)

