import requests
from rest_framework.exceptions import ValidationError
from decouple import config

class CloudflareTurnstile:
    VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    
    @classmethod
    def verify_token(cls, token, ip_address=None):
        # Obtenemos la clave secreta desde .env usando python-decouple
        secret_key = config('CF_TURNSTILE_SECRET_KEY', default='')
        
        # Si no hay clave configurada, consideramos la verificación como exitosa
        if not secret_key:
            return True 
            
        data = {
            'secret': secret_key,  # Usamos la variable obtenida de .env
            'response': token
        }
        
        if ip_address:
            data['remoteip'] = ip_address
            
        try:
            response = requests.post(cls.VERIFY_URL, data=data, timeout=5)
            result = response.json()
            
            if not result.get('success'):
                error_codes = result.get('error-codes', ['unknown'])
                raise ValidationError({
                    'cf_turnstile_response': f"Error en verificación Turnstile: {', '.join(error_codes)}"
                })
                
            return True
        except requests.RequestException as e:
            raise ValidationError({
                'cf_turnstile_response': "Error al conectar con el servicio de verificación"
            })