from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from users.serializers import UserSerializer, UserListSerializer, UserDetalleSerializer, CustomTokenObtainPairSerializer, CustomUserSerializer
from django.shortcuts import get_object_or_404
from users.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

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
            return Response({'message':'Usuario registrado'}, status=status.HTTP_201_CREATED)
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

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh-token': login_serializer.validated_data.get('refresh'),
                    'user':user_serializer.data
                }, status=status.HTTP_200_OK)
            return Response({'error':'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
