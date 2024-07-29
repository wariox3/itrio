import secrets
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from seguridad.models import User
from contenedor.models import Contenedor, UsuarioContenedor, CtnVerificacion
from contenedor.serializers.contenedor import ContenedorSerializador
from contenedor.serializers.usuario_contenedor import UsuarioContenedorSerializador, UsuarioContenedorConsultaContenedorSerializador
from contenedor.serializers.verificacion import CtnVerificacionSerializador
from datetime import datetime, timedelta
from decouple import config
from utilidades.zinc import Zinc

class UsuarioContenedorViewSet(viewsets.ModelViewSet):
    queryset = UsuarioContenedor.objects.all()
    serializer_class = UsuarioContenedorSerializador    
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        usuarioEmpresa = self.get_object()
        if usuarioEmpresa.rol == 'invitado':
            self.perform_destroy(usuarioEmpresa)
            empresa = Contenedor.objects.get(pk=usuarioEmpresa.contenedor_id)
            empresa.usuarios -= 1
            empresa.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'mensaje':"El usuario propietario no se puede eliminar", 'codigo': 22}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'invitar',)
    def invitar(self, request):
        try:
            raw = request.data
            invitado = raw.get('invitado')
            contenedor_id = raw.get('contenedor_id')
            usuario_id = raw.get('usuario_id')
            if invitado and contenedor_id and usuario_id:
                contenedor = Contenedor.objects.get(pk=contenedor_id)
                usuario = User.objects.get(pk=usuario_id)
                token = secrets.token_urlsafe(20)            
                raw["token"] = token
                raw["vence"] = datetime.now().date() + timedelta(days=1)
                raw["contenedor_id"] = contenedor.id
                raw["usuario_invitado_username"] = invitado
                if User.objects.filter(username=invitado).exists():
                    usuarioInvitado = User.objects.get(username = invitado)
                    if usuarioInvitado.id == usuario.id:
                        return Response({'mensaje':'El usuario no se puede invitar a el mismo', 'codigo':18}, status=status.HTTP_400_BAD_REQUEST)
                    if UsuarioContenedor.objects.filter(usuario_id=usuarioInvitado.id, contenedor_id=contenedor.id).exists():
                        return Response({'mensaje':'El usuario ya esta confirmado para esta empresa', 'codigo':20}, status=status.HTTP_400_BAD_REQUEST)
                if contenedor.plan:
                    if contenedor.plan.limite_usuarios > 0:
                        if contenedor.plan.limite_usuarios >= contenedor.usuarios:
                            return Response({'mensaje':'La empresa supera el numero de usuarios segun el plan, si quiere invitar nuevos usuarios debe incrementar el plan', 'codigo':20}, status=status.HTTP_400_BAD_REQUEST)
                verificacionSerializador = CtnVerificacionSerializador(data = raw)
                if verificacionSerializador.is_valid():                                             
                    verificacionSerializador.save()                    
                    url = f"https://{config('DOMINIO_FRONTEND')}/auth/login/" + token
                    html_content = """
                                <h1>¡Hola {usuario}!</h1>
                                <p>Te han invitado para que seas parte de un equipo de trabajo en RedDoc. Clic en el siguiente enlace 
                                para aceptar la invitacion</p>
                                <a href='{url}' class='button'>Aceptar invitacion</a>
                                """.format(url=url, usuario=invitado)
                    correo = Zinc()  
                    correo.correo_reddoc(invitado, 'Invitacion a RedDoc', html_content)
                    return Response({'verificacion': verificacionSerializador.data}, status=status.HTTP_201_CREATED)
                return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':3, 'validaciones': verificacionSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)                    
            else:
                return Response({'mensaje':'Faltal parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                
        except User.DoesNotExist:
            return Response({'mensaje':'El usuario no existe', 'codigo':8}, status=status.HTTP_400_BAD_REQUEST)
        except Contenedor.DoesNotExist:
            return Response({'mensaje':'El contenedor no existe', 'codigo':8}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=False, methods=["post"], url_path=r'confirmar',)
    def confirmar(self, request):
        usuarioSesion = request.user
        try:
            raw = request.data
            token = raw.get('token')
            verificacion = CtnVerificacion.objects.get(token=token)
            if verificacion.estado_usado == False:
                if User.objects.filter(username=verificacion.usuario_invitado_username).exists():
                    usuario = User.objects.get(username=verificacion.usuario_invitado_username)                
                    if not UsuarioContenedor.objects.filter(usuario_id=usuario.id, contenedor_id=verificacion.contenedor_id).exists():
                        if usuario.id == usuarioSesion.id:
                            data = {'usuario': usuario.id, 'contenedor': verificacion.contenedor_id, 'rol':'invitado'}
                            usuarioContenedorSerializador = UsuarioContenedorSerializador(data=data)            
                            if usuarioContenedorSerializador.is_valid():
                                usuarioContenedorSerializador.save()
                                verificacion.estado_usado = True
                                verificacion.save()
                                contenedor = Contenedor.objects.get(pk=verificacion.contenedor_id) 
                                contenedor.usuarios += 1
                                contenedor.save()
                                return Response({'confirmar': True}, status=status.HTTP_200_OK)
                            return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':19, 'validaciones': usuarioContenedorSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'mensaje':"El usuario que inicio sesion no es el usuario invitado", 'codigo': 21}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'mensaje':'El usuario ya esta confirmado para esta empresa', 'codigo':20}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje':"El usuario invitado no existe", 'codigo': 15}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'mensaje':"El token ya fue usado", 'codigo': 6}, status=status.HTTP_400_BAD_REQUEST)
        except CtnVerificacion.DoesNotExist:
            return Response({'mensaje':"La verificacion no existe", 'codigo': 15}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"], url_path=r'validar',)
    def validar(self, request):
        raw = request.data
        usuario_id = raw.get('usuario')
        contenedor_id = raw.get('contenedor_id')
        if usuario_id and contenedor_id:            
            if UsuarioContenedor.objects.filter(usuario_id=usuario_id, contenedor_id=contenedor_id).exists():                
                contenedor = Contenedor.objects.get(pk=contenedor_id)
                contenedorSerializador = ContenedorSerializador(contenedor)
                return Response({'validar': True, 'empresa': contenedorSerializador.data}, status=status.HTTP_200_OK)                
            else:
                return Response({'validar': False}, status=status.HTTP_200_OK) 
        else:
            return Response({'mensaje':"Faltan parametros", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], url_path=r'consulta-contenedor',)
    def consulta_contenedor(self, request):
        raw = request.data
        contenedor_id = raw.get('contenedor_id')
        if contenedor_id:  
            usuarioContenedor = UsuarioContenedor.objects.filter(contenedor_id=contenedor_id).order_by('-rol', 'contenedor__nombre')                         
            usuarioContenedorSerializer = UsuarioContenedorConsultaContenedorSerializador(usuarioContenedor, many=True)
            return Response({'usuarios': usuarioContenedorSerializer.data}, status=status.HTTP_200_OK)                
        else:
            return Response({'mensaje':"Faltan parametros", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], url_path=r'consulta-usuario',)
    def consulta_usuario(self, request):
        raw = request.data
        usuario_id = raw.get('usuario_id')
        reddoc = raw.get('reddoc')
        ruteo = raw.get('ruteo')
        if usuario_id and (reddoc or ruteo):  
            usuarioEmpresa = UsuarioContenedor.objects.filter(usuario_id=usuario_id).order_by('-rol', 'contenedor__nombre')                         
            if reddoc:
                usuarioEmpresa = usuarioEmpresa.filter(contenedor__reddoc=reddoc)
            if ruteo:
                usuarioEmpresa = usuarioEmpresa.filter(contenedor__ruteo=ruteo)
            usuarioEmpresaSerializer = UsuarioContenedorSerializador(usuarioEmpresa, many=True)
            return Response({'contenedores': usuarioEmpresaSerializer.data}, status=status.HTTP_200_OK)                
        else:
            return Response({'mensaje':"Faltan parametros", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)        