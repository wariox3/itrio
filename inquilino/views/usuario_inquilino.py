import secrets
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from seguridad.models import User
from inquilino.models import Inquilino, UsuarioInquilino, Verificacion
from inquilino.serializers.inquilino import InquilinoSerializador
from inquilino.serializers.usuario_inquilino import UsuarioInquilinoSerializador, UsuarioInquilinoConsultaInquilinoSerializador
from inquilino.serializers.verificacion import VerificacionSerializador
from datetime import datetime, timedelta
from utilidades.correo import Correo

class UsuarioInquilinoViewSet(viewsets.ModelViewSet):
    queryset = UsuarioInquilino.objects.all()
    serializer_class = UsuarioInquilinoSerializador    
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        usuarioEmpresa = self.get_object()
        if usuarioEmpresa.rol == 'invitado':
            self.perform_destroy(usuarioEmpresa)
            empresa = Inquilino.objects.get(pk=usuarioEmpresa.inquilino_id)
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
            inquilino_id = raw.get('inquilino_id')
            usuario_id = raw.get('usuario_id')
            if invitado and inquilino_id and usuario_id:
                inquilino = Inquilino.objects.get(pk=inquilino_id)
                usuario = User.objects.get(pk=usuario_id)
                token = secrets.token_urlsafe(20)            
                raw["token"] = token
                raw["vence"] = datetime.now().date() + timedelta(days=1)
                raw["inquilino_id"] = inquilino.id
                raw["usuario_invitado_username"] = invitado
                if User.objects.filter(username=invitado).exists():
                    usuarioInvitado = User.objects.get(username = invitado)
                    if usuarioInvitado.id == usuario.id:
                        return Response({'mensaje':'El usuario no se puede invitar a el mismo', 'codigo':18}, status=status.HTTP_400_BAD_REQUEST)
                    if UsuarioInquilino.objects.filter(usuario_id=usuarioInvitado.id, inquilino_id=inquilino.id).exists():
                        return Response({'mensaje':'El usuario ya esta confirmado para esta empresa', 'codigo':20}, status=status.HTTP_400_BAD_REQUEST)
                if inquilino.plan:
                    if inquilino.plan.limite_usuarios > 0:
                        if inquilino.plan.limite_usuarios >= inquilino.usuarios:
                            return Response({'mensaje':'La empresa supera el numero de usuarios segun el plan, si quiere invitar nuevos usuarios debe incrementar el plan', 'codigo':20}, status=status.HTTP_400_BAD_REQUEST)
                verificacionSerializador = VerificacionSerializador(data = raw)
                if verificacionSerializador.is_valid():                                             
                    verificacionSerializador.save()
                    correo = Correo()               
                    contenido = 'Siga este enlace para aceptar la invitacion http://muup.online/auth/login/' + token                    
                    correo.enviar(invitado, 'Invitacion a redoffice', contenido)                                            
                    return Response({'verificacion': verificacionSerializador.data}, status=status.HTTP_201_CREATED)
                return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':3, 'validaciones': verificacionSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)                    
            else:
                return Response({'mensaje':'Faltal parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                
        except User.DoesNotExist:
            return Response({'mensaje':'El usuario no existe', 'codigo':8}, status=status.HTTP_400_BAD_REQUEST)
        except Inquilino.DoesNotExist:
            return Response({'mensaje':'La empresa no existe', 'codigo':8}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=False, methods=["post"], url_path=r'confirmar',)
    def confirmar(self, request):
        usuarioSesion = request.user
        try:
            raw = request.data
            token = raw.get('token')
            verificacion = Verificacion.objects.get(token=token)
            if verificacion.estado_usado == False:
                if User.objects.filter(username=verificacion.usuario_invitado_username).exists():
                    usuario = User.objects.get(username=verificacion.usuario_invitado_username)                
                    if not UsuarioInquilino.objects.filter(usuario_id=usuario.id, inquilino_id=verificacion.inquilino_id).exists():
                        if usuario.id == usuarioSesion.id:
                            data = {'usuario': usuario.id, 'inquilino': verificacion.inquilino_id, 'rol':'invitado'}
                            usuarioInquilinoSerializador = UsuarioInquilinoSerializador(data=data)            
                            if usuarioInquilinoSerializador.is_valid():
                                usuarioInquilinoSerializador.save()
                                verificacion.estado_usado = True
                                verificacion.save()
                                inquilino = Inquilino.objects.get(pk=verificacion.inquilino_id) 
                                inquilino.usuarios += 1
                                inquilino.save()
                                return Response({'confirmar': True}, status=status.HTTP_200_OK)
                            return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':19, 'validaciones': usuarioInquilinoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'mensaje':"El usuario que inicio sesion no es el usuario invitado", 'codigo': 21}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'mensaje':'El usuario ya esta confirmado para esta empresa', 'codigo':20}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje':"El usuario invitado no existe", 'codigo': 15}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'mensaje':"El token ya fue usado", 'codigo': 6}, status=status.HTTP_400_BAD_REQUEST)
        except Verificacion.DoesNotExist:
            return Response({'mensaje':"La verificacion no existe", 'codigo': 15}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"], url_path=r'validar',)
    def validar(self, request):
        raw = request.data
        usuario_id = raw.get('usuario')
        inquilino_id = raw.get('inquilino_id')
        if usuario_id and inquilino_id:            
            if UsuarioInquilino.objects.filter(usuario_id=usuario_id, inquilino_id=inquilino_id).exists():                
                inquilino = Inquilino.objects.get(pk=inquilino_id)
                inquilinoSerializador = InquilinoSerializador(inquilino)
                return Response({'validar': True, 'empresa': inquilinoSerializador.data}, status=status.HTTP_200_OK)                
            else:
                return Response({'validar': False}, status=status.HTTP_200_OK) 
        else:
            return Response({'mensaje':"Faltan parametros", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], url_path=r'consulta-inquilino',)
    def consulta_inquilino(self, request):
        raw = request.data
        inquilino_id = raw.get('inquilino_id')
        if inquilino_id:  
            usuarioInquilino = UsuarioInquilino.objects.filter(inquilino_id=inquilino_id).order_by('-rol')                         
            usuarioInquilinoSerializer = UsuarioInquilinoConsultaInquilinoSerializador(usuarioInquilino, many=True)
            return Response({'usuarios': usuarioInquilinoSerializer.data}, status=status.HTTP_200_OK)                
        else:
            return Response({'mensaje':"Faltan parametros", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], url_path=r'consulta-usuario',)
    def consulta_usuario(self, request):
        raw = request.data
        usuario_id = raw.get('usuario_id')
        if usuario_id:  
            usuarioEmpresa = UsuarioInquilino.objects.filter(usuario_id=usuario_id).order_by('-rol')                         
            usuarioEmpresaSerializer = UsuarioInquilinoSerializador(usuarioEmpresa, many=True)
            return Response({'empresas': usuarioEmpresaSerializer.data}, status=status.HTTP_200_OK)                
        else:
            return Response({'mensaje':"Faltan parametros", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)        