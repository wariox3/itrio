import secrets
from rest_framework import status, viewsets
from rest_framework.response import Response
from seguridad.serializers import VerificacionSerializer
from seguridad.models import User, Verificacion, UsuarioEmpresa
from inquilino.models import Empresa
from datetime import datetime, timedelta
from utilidades.correo import Correo
from rest_framework.decorators import action

class VerificacionViewSet(viewsets.ModelViewSet):
    queryset = Verificacion.objects.all()
    serializer_class = VerificacionSerializer

    def create(self, request):
        try:
            raw = request.data
            accion = raw.get('accion')
            token = secrets.token_urlsafe(20)            
            raw["token"] = token
            raw["vence"] = datetime.now().date() + timedelta(days=1)
            invitado = raw.get('invitado')
            if accion == 'clave' or accion == 'registro':
                usuario = User.objects.get(username = raw.get('username'))
                raw["usuario_id"] = usuario.id
            if accion == 'invitar':
                empresa = Empresa.objects.get(pk=raw.get('empresa_id'))
                usuario = User.objects.get(pk=raw.get('usuario_id'))
                raw["empresa_id"] = empresa.id
                if invitado:
                    raw["usuario_invitado_username"] = invitado
                    if User.objects.filter(username=invitado).exists():
                        usuarioInvitado = User.objects.get(username = invitado)
                        if usuarioInvitado.id == usuario.id:
                            return Response({'mensaje':'El usuario no se puede invitar a el mismo', 'codigo':18}, status=status.HTTP_400_BAD_REQUEST)
                        if UsuarioEmpresa.objects.filter(usuario_id=usuarioInvitado.id, empresa_id=empresa.id).exists():
                            return Response({'mensaje':'El usuario ya esta confirmado para esta empresa', 'codigo':20}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje':'Debe especificar el correo para invitar', 'codigo':16}, status=status.HTTP_400_BAD_REQUEST)                
            verificacion_serializer = VerificacionSerializer(data = raw)
            if verificacion_serializer.is_valid():                                             
                verificacion_serializer.save()
                correo = Correo()
                if accion == 'registro':                
                    contenido='Enlace para verificar http://muup.online/auth/verificacion/' + token                    
                    correo.enviar(usuario.correo, 'Debe verificar su cuenta redoffice', contenido)   
                if accion == 'clave':
                    contenido='Enlace para cambiar la clave http://muup.online/auth/clave/cambiar/' + token
                    correo.enviar(usuario.correo, 'Debe verificar su cuenta redoffice', contenido) 
                if accion == 'invitar':                
                    contenido = 'Siga este enlace para aceptar la invitacion https://muup.online/auth/login/' + token                    
                    correo.enviar(invitado, 'Invitacion a redoffice', contenido)                                            
                return Response({'verificacion': verificacion_serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':3, 'validaciones': verificacion_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'mensaje':'El usuario no existe', 'codigo':8}, status=status.HTTP_400_BAD_REQUEST)
        except Empresa.DoesNotExist:
            return Response({'mensaje':'La empresa no existe', 'codigo':8}, status=status.HTTP_400_BAD_REQUEST)                

    @action(detail=False, methods=["post"], url_path=r'token',)
    def token(self, request):
        tokenUrl = request.data.get('token')
        verificacion = Verificacion.objects.filter(token=tokenUrl).first()
        if verificacion:
            if verificacion.estado_usado == False:
                fechaActual = datetime.now().date()                
                if fechaActual <= verificacion.vence:
                    verificacion.estado_usado = True
                    verificacion.save()
                    usuario = User.objects.get(id = verificacion.usuario_id)
                    usuario.is_active = True
                    usuario.save()
                    verificacionSerializer = VerificacionSerializer(verificacion)                
                    return Response({'verificado': True, 'verificacion': verificacionSerializer.data}, status=status.HTTP_200_OK)
                return Response({'mensaje':'El token de la verificacion esta vencido', 'codigo': 6, 'codigoUsuario': verificacion.usuario_id}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'mensaje':'La verificacion ya fue usada', 'codigo': 5, 'codigoUsuario': verificacion.usuario_id}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje':'No se ha encontrado la verificacion', 'codigo': 4}, status=status.HTTP_400_BAD_REQUEST)