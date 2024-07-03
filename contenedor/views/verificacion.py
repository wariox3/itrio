from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from contenedor.serializers.verificacion import VerificacionSerializador
from contenedor.models import Verificacion
from seguridad.models import User
from rest_framework.decorators import action
import secrets
from decouple import config
from datetime import datetime, timedelta
from utilidades.zinc import Zinc

class VerificacionViewSet(viewsets.ModelViewSet):
    queryset = Verificacion.objects.all()
    serializer_class = VerificacionSerializador

    @action(detail=False, methods=["post"], url_path=r'reenviar-verificacion',)
    def reenviar_verificacion(self, request):
        usuario_id = request.data.get('usuario_id')
        usuario = User.objects.get(pk=usuario_id)
        token = secrets.token_urlsafe(20)                           
        datos = {
            'usuario_id': usuario.id,
            'token': token,
            'vence': datetime.now().date() + timedelta(days=1)
        }
        
        verificacion_serializer = VerificacionSerializador(data = datos)                                           
        if verificacion_serializer.is_valid():
            verificacion_serializer.save()
            dominio = config('DOMINIO_FRONTEND')                
            url = 'https://' + dominio + '/auth/verificacion/' + token
            html_content = """
                            <h1>¡Hola {usuario}!</h1>
                            <p>Estamos comprometidos con la seguridad de tu cuenta, por esta razón necesitamos que nos valides 
                            que eres tú, por favor verifica tu cuenta haciendo clic en el siguiente enlace.</p>
                            <a href='{url}' class='button'>Verificar cuenta</a>
                            """.format(url=url, usuario=usuario.nombre_corto)
            correo = Zinc()  
            correo.correo_reddoc(usuario.correo, 'Verificar cuenta de RedDoc', html_content)  
            return Response({'verificacion': verificacion_serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':3, 'validaciones': verificacion_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        