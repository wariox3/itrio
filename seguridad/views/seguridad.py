from rest_framework import status
from django.conf import settings
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from seguridad.serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from .turnstile import CloudflareTurnstile
from decouple import config
    
class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        turnstile_token = request.data.get('cf_turnstile_response', '')
        
        turnstile_secret_key = config('CF_TURNSTILE_SECRET_KEY', default='')
        if turnstile_secret_key:
            client_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
            turnstile_valid = CloudflareTurnstile.verify_token(turnstile_token, client_ip)
            
            if not turnstile_valid:
                return Response({
                    'error': 'Error en la verificación de Turnstile',
                    'codigo': 8 
                }, status=status.HTTP_400_BAD_REQUEST)

        # Autenticación normal
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)

        if user is not None:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = UserSerializer(user)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh-token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                'error': 'Contraseña o nombre de usuario incorrectos',
                'codigo': 7
            }, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
            'mensaje': 'Contraseña o nombre de usuario incorrectos',
            'codigo': 7
        }, status=status.HTTP_400_BAD_REQUEST)