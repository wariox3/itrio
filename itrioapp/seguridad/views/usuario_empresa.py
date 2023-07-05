from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from seguridad.models import UsuarioEmpresa, Verificacion, User
from inquilino.models import Empresa
from seguridad.serializers import UsuarioEmpresaSerializador
from inquilino.serializers import EmpresaSerializer


class UsuarioEmpresaViewSet(viewsets.ModelViewSet):
    queryset = UsuarioEmpresa.objects.all()
    serializer_class = UsuarioEmpresaSerializador    
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'confirmar',)
    def confirmar(self, request):
        try:
            raw = request.data
            token = raw.get('token')
            verificacion = Verificacion.objects.get(token=token)
            if User.objects.filter(username=verificacion.usuario_invitado_username).exists():
                usuario = User.objects.get(username=verificacion.usuario_invitado_username)                
                data = {'usuario': usuario.id, 'empresa': verificacion.empresa_id, 'rol':'invitado'}
                usuario_empresa_serializador = UsuarioEmpresaSerializador(data=data)            
                if usuario_empresa_serializador.is_valid():
                    usuario_empresa_serializador.save() 
                    return Response({'confirmar': True}, status=status.HTTP_200_OK)
                return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':19, 'validaciones': usuario_empresa_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje':"El usuario invitado no existe", 'codigo': 15}, status=status.HTTP_404_NOT_FOUND)
        except Verificacion.DoesNotExist:
            return Response({'mensaje':"La verificacion no existe", 'codigo': 15}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"], url_path=r'validar',)
    def validar(self, request):
        raw = request.data
        usuario_id = raw.get('usuario')
        empresa_id = raw.get('empresa')
        if usuario_id and empresa_id:            
            if UsuarioEmpresa.objects.filter(usuario_id=usuario_id, empresa_id=empresa_id).exists():                
                empresa = Empresa.objects.get(pk=empresa_id)
                empresaSerializer = EmpresaSerializer(empresa)
                return Response({'validar': True, 'empresa': empresaSerializer.data}, status=status.HTTP_200_OK)                
            else:
                return Response({'validar': False}, status=status.HTTP_200_OK) 
        else:
            return Response({'mensaje':"Faltan parametros", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)