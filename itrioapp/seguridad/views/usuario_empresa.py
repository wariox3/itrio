from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from seguridad.models import UsuarioEmpresa, Verificacion, User

from seguridad.serializers import UsuarioEmpresaSerializador


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
                data = {'usuario': usuario.id, 'empresa': verificacion.empresa_id}
                usuario_empresa_serializador = UsuarioEmpresaSerializador(data=data)            
                if usuario_empresa_serializador.is_valid():
                    usuario_empresa_serializador.save() 
                    return Response({'confirmar': True}, status=status.HTTP_200_OK)
                return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':19, 'validaciones': usuario_empresa_serializador.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje':"El usuario invitado no existe", 'codigo': 15}, status=status.HTTP_404_NOT_FOUND)
        except Verificacion.DoesNotExist:
            return Response({'mensaje':"La verificacion no existe", 'codigo': 15}, status=status.HTTP_404_NOT_FOUND)