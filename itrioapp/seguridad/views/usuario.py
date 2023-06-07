from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from seguridad.serializers import UserSerializer, UserUpdateSerializer, UserListSerializer, UserDetalleSerializer, UsuarioEmpresaSerializador
from django.shortcuts import get_object_or_404
from seguridad.models import User, UsuarioEmpresa
from .verificacion import VerificacionNuevo
from django.core.management import call_command
from decouple import config

class UsuarioViewSet(GenericViewSet, UpdateModelMixin):
    model = User
    queryset = None
    serializer_class = UserSerializer
    detalle_serializer_class = UserDetalleSerializer
    
    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def list(self, request):        
        queryset = User.objects.all()
        serializer_class = UserListSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            #Enviar verificacion (metodo)
            request.data['username'] = user.username
            request.data['accion'] = 'registro'
            verificacionAPIView = VerificacionNuevo()
            verificacionAPIView.post(request)
            return Response({'usuario': user_serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'mensaje':'Errores en el registro del usuario', 'codigo':2, 'validaciones': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.detalle_serializer_class(user)
        return Response(user_serializer.data)

    def update(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = UserUpdateSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'actualizacion': True, 'usuario': user_serializer.data}, status=status.HTTP_201_CREATED)            
        return Response({'mensaje':'Errores en la actualizacion del usuario', 'codigo':10, 'validaciones': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ClaveCambiar(APIView):

    def post(self, request):    
        codigoUsuario = request.data.get('id')
        clave = request.data.get('password')
        usuario = User.objects.get(id = codigoUsuario)
        usuario.set_password(clave)
        usuario.save()
        return Response({'cambio': True}, status=status.HTTP_200_OK)

class UsuarioEmpresaAPIView(APIView):

    def get(self, request, usuario_id): 
        queryset = UsuarioEmpresa.objects.filter(usuario_id = usuario_id)
        serializer_class = UsuarioEmpresaSerializador(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

class EmpresaNuevoAPIView(APIView):

    def post(self, request): 
        try:            
            empresa = request.data.get('empresa')
            usuario = request.data.get('usuario')
            if empresa and usuario:
                #buscar que empresa no exista  one_entry = Entry.objects.get(pk=1)
                if config('ENV') == 'dev':
                    dominio = '.localhost'
                else:
                    dominio = '.muup.online'                
                call_command('create_tenant', schema_name=empresa, domain_domain=empresa+dominio, domain_is_primary='0') 
                #buscar la empresa que se creo filter por schema_name -> tabla empresa
                #crea usuario_empresa
                #request.data['usuario'] = usuario
                #request.data['empresa'] = 'registro'
                #verificacionAPIView = VerificacionNuevo() -> la clase para crear automatica 
                #verificacionAPIView.post(request)
                return Response({'empresa': True}, status=status.HTTP_200_OK)            
            return Response({'mensaje': "Debe suministrar empresa y usuario"}, status=status.HTTP_400_BAD_REQUEST)            
        except FileNotFoundError:
            return Response({'mensaje': True}, status=status.HTTP_400_BAD_REQUEST)            
        