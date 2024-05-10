from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == 404:
            response.data = {
                'mensaje': 'No existe',
                'codigo': 15
            }
        if response.status_code == 400:
            response.data = {
                'mensaje': 'Mensajes de validación',
                'codigo': 14,
                'validacion': response.data
            }            
    return response