from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from decouple import config
import logging  # Añade esto para logging

from seguridad.serializers import CustomTokenObtainPairSerializer, UserSerializer
from .turnstile import CloudflareTurnstile

logger = logging.getLogger(__name__)  # Añade esto

class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            # 1. Obtener datos de la solicitud
            turnstile_token = request.data.get('cf_turnstile_response', '')
            proyecto = request.data.get('proyecto', 'REDDOC').upper()
            auth_interna = request.headers.get('X-Internal-Auth') == config('AUT_INTERNA')
            
            # 2. Validar proyecto
            proyectos_validos = ['REDDOC', 'RUTEO', 'POS', 'RUTEOAPP', 'CUENTA', 'TRANSPORTE', 'TURNOS', 'CLIENTE']
            if proyecto not in proyectos_validos:
                return Response({
                    'error': 'Proyecto no válido',
                    'codigo': 9,
                    'proyectos_validos': proyectos_validos
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 3. Obtener configuración
            turnstile_secret_key = config(f'CF_TURNSTILE_SECRET_KEY_{proyecto}', default='')
            env = config('ENV', default='prod').lower()
            
            # 4. Configuración de bypass (NUEVO)
            # BYPASS_TURNSTILE = true/false → Desactiva COMPLETAMENTE Turnstile
            # TURNSTILE_FALLBACK = true/false → Permite continuar si Turnstile está caído
            bypass_turnstile = config('BYPASS_TURNSTILE', default='false').lower() == 'true'
            turnstile_fallback = config('TURNSTILE_FALLBACK', default='false').lower() == 'true'

            # 5. Decidir si validar Turnstile
            should_validate_turnstile = (
                env not in ['dev', 'test'] 
                and turnstile_secret_key 
                and proyecto != 'RUTEOAPP' 
                and not auth_interna
                and not bypass_turnstile  # ← Si bypass_turnstile=True, NO se valida
            )
            
            # 6. Validar Turnstile (si corresponde)
            if should_validate_turnstile:
                client_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
                try:
                    # Llama a verify_token con allow_fallback
                    CloudflareTurnstile.verify_token(
                        turnstile_token, 
                        turnstile_secret_key, 
                        client_ip,
                        allow_fallback=turnstile_fallback  # ← Este parámetro es nuevo
                    )
                except ValidationError as e:
                    # Si hay error de conexión y fallback está habilitado, continuar
                    error_str = str(e.detail).lower()
                    if turnstile_fallback and any(keyword in error_str for keyword in ['conexión', 'connection', 'timeout', 'conectar']):
                        logger.warning(f"Turnstile caído (error HTTP), continuando con autenticación: {str(e.detail)}")
                        # NO retorna error, continúa con la autenticación normal
                    else:
                        # Para otros errores (token inválido, etc.) sí retorna error
                        return Response({
                            'error': 'Error en la verificación de Turnstile',
                            'detalle': str(e.detail),
                            'codigo': 8
                        }, status=status.HTTP_400_BAD_REQUEST)
            
            # 7. Resto de la lógica de autenticación (usuario y contraseña)
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