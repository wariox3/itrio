import secrets
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from seguridad.models import User
from inquilino.models import Inquilino, UsuarioInquilino, Verificacion
from inquilino.serializers.inquilino import InquilinoSerializador
from inquilino.serializers.usuario_inquilino import UsuarioInquilinoSerializador, UsuarioInquilinoConsultaInquilinoSerializador
from inquilino.serializers.verificacion import VerificacionSerializer
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
                empresa = Inquilino.objects.get(pk=inquilino_id)
                usuario = User.objects.get(pk=usuario_id)
                token = secrets.token_urlsafe(20)            
                raw["token"] = token
                raw["vence"] = datetime.now().date() + timedelta(days=1)
                raw["inquilino_id"] = empresa.id
                raw["usuario_invitado_username"] = invitado
                if User.objects.filter(username=invitado).exists():
                    usuarioInvitado = User.objects.get(username = invitado)
                    if usuarioInvitado.id == usuario.id:
                        return Response({'mensaje':'El usuario no se puede invitar a el mismo', 'codigo':18}, status=status.HTTP_400_BAD_REQUEST)
                    if UsuarioInquilino.objects.filter(usuario_id=usuarioInvitado.id, inquilino_id=empresa.id).exists():
                        return Response({'mensaje':'El usuario ya esta confirmado para esta empresa', 'codigo':20}, status=status.HTTP_400_BAD_REQUEST)
                if empresa.plan:
                    if empresa.plan.limite_usuarios > 0:
                        if empresa.plan.limite_usuarios >= empresa.usuarios:
                            return Response({'mensaje':'La empresa supera el numero de usuarios segun el plan, si quiere invitar nuevos usuarios debe incrementar el plan', 'codigo':20}, status=status.HTTP_400_BAD_REQUEST)
                verificacion_serializer = VerificacionSerializer(data = raw)
                if verificacion_serializer.is_valid():                                             
                    verificacion_serializer.save()
                    correo = Correo()               
                    contenido = 'Siga este enlace para aceptar la invitacion http://muup.online/auth/login/' + token                    
                    correo.enviar(invitado, 'Invitacion a redoffice', contenido)                                            
                    return Response({'verificacion': verificacion_serializer.data}, status=status.HTTP_201_CREATED)
                return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':3, 'validaciones': verificacion_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)                    
            else:
                return Response({'mensaje':'Faltal parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                
        except User.DoesNotExist:
            return Response({'mensaje':'El usuario no existe', 'codigo':8}, status=status.HTTP_400_BAD_REQUEST)
        except Inquilino.DoesNotExist:
            return Response({'mensaje':'La empresa no existe', 'codigo':8}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=False, methods=["post"], url_path=r'confirmar',)
    def confirmar(self, request):
        usuarioSesion = request.user
        #return Response("Hola mundo" + str(Usuario.id),status=status.HTTP_200_OK)
        try:
            raw = request.data
            token = raw.get('token')
            verificacion = Verificacion.objects.get(token=token)
            if verificacion.estado_usado == False:
                if User.objects.filter(username=verificacion.usuario_invitado_username).exists():
                    usuario = User.objects.get(username=verificacion.usuario_invitado_username)                
                    if not UsuarioInquilino.objects.filter(usuario_id=usuario.id, inquilino_id=verificacion.inquilino_id).exists():
                        if usuario.id == usuarioSesion.id:
                            data = {'usuario': usuario.id, 'empresa': verificacion.inquilino_id, 'rol':'invitado'}
                            usuario_empresa_serializador = UsuarioInquilinoSerializador(data=data)            
                            if usuario_empresa_serializador.is_valid():
                                usuario_empresa_serializador.save()
                                verificacion.estado_usado = True
                                verificacion.save()
                                empresa = Inquilino.objects.get(pk=verificacion.inquilino_id) 
                                empresa.usuarios += 1
                                empresa.save()
                                return Response({'confirmar': True}, status=status.HTTP_200_OK)
                            return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':19, 'validaciones': usuario_empresa_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)
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
        inquilino_id = raw.get('empresa')
        if usuario_id and inquilino_id:            
            if UsuarioInquilino.objects.filter(usuario_id=usuario_id, inquilino_id=inquilino_id).exists():                
                empresa = Inquilino.objects.get(pk=inquilino_id)
                empresaSerializer = InquilinoSerializador(empresa)
                return Response({'validar': True, 'empresa': empresaSerializer.data}, status=status.HTTP_200_OK)                
            else:
                return Response({'validar': False}, status=status.HTTP_200_OK) 
        else:
            return Response({'mensaje':"Faltan parametros", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], url_path=r'consulta-empresa',)
    def consulta_empresa(self, request):
        raw = request.data
        inquilino_id = raw.get('inquilino_id')
        if inquilino_id:  
            usuarioEmpresa = UsuarioInquilino.objects.filter(inquilino_id=inquilino_id).order_by('-rol')                         
            usuarioEmpresaSerializer = UsuarioInquilinoConsultaInquilinoSerializador(usuarioEmpresa, many=True)
            return Response({'usuarios': usuarioEmpresaSerializer.data}, status=status.HTTP_200_OK)                
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