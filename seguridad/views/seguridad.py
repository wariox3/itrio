from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from decouple import config
from seguridad.serializers import CustomTokenObtainPairSerializer, UserSerializer
from .turnstile import CloudflareTurnstile

class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            turnstile_token = request.data.get('cf_turnstile_response', '')
            proyecto = request.data.get('proyecto', 'REDDOC').upper()  # Aseguramos mayúsculas
            
            # Validar proyecto
            proyectos_validos = ['REDDOC', 'RUTEO', 'POS']
            if proyecto not in proyectos_validos:
                return Response({
                    'error': 'Proyecto no válido',
                    'codigo': 9,
                    'proyectos_validos': proyectos_validos
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Obtener secret key para el proyecto
            turnstile_secret_key = config(f'CF_TURNSTILE_SECRET_KEY_{proyecto}', default='')
            
            if turnstile_secret_key:
                client_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
                try:
                    CloudflareTurnstile.verify_token(turnstile_token, turnstile_secret_key, client_ip)
                except ValidationError as e:
                    return Response({
                        'error': 'Error en la verificación de Turnstile',
                        'detalle': str(e.detail),
                        'codigo': 8 
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Autenticación de usuario
            username = request.data.get('username', '').strip()
            password = request.data.get('password', '').strip()
            
            if not username or not password:
                return Response({
                    'error': 'Usuario y contraseña son requeridos',
                    'codigo': 10
                }, status=status.HTTP_400_BAD_REQUEST)
                
            user = authenticate(username=username, password=password)
            
            if user is None:
                return Response({
                    'error': 'Credenciales inválidas',
                    'codigo': 7
                }, status=status.HTTP_400_BAD_REQUEST)
                
            # Generar tokens
            login_serializer = self.serializer_class(data=request.data)
            login_serializer.is_valid(raise_exception=True)
            user_serializer = UserSerializer(user)
            
            return Response({
                'token': login_serializer.validated_data.get('access'),
                'refresh-token': login_serializer.validated_data.get('refresh'),
                'user': user_serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'Error interno del servidor',
                'detalle': str(e),
                'codigo': 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)