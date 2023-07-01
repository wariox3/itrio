from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from seguridad.serializers import UserSerializer, UserUpdateSerializer, UserListSerializer, UserDetalleSerializer, UsuarioEmpresaSerializador
from django.shortcuts import get_object_or_404
from seguridad.models import User, UsuarioEmpresa
from seguridad.views.usuario_empresa import UsuarioEmpresaViewSet
from inquilino.models import Empresa
from .verificacion import VerificacionViewSet
from django.core.management import call_command
import os
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
            verificacionAPIView = VerificacionViewSet()
            verificacionAPIView.create(request)
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
            subdominio = request.data.get('subdominio')
            parametroUsuario = request.data.get('usuario')
            nombre = request.data.get('nombre')
            imagen = request.data.get('imagen')
            if subdominio and parametroUsuario and nombre:
                empresaValidacion = Empresa.objects.filter(**{'schema_name':subdominio})
                if empresaValidacion:
                    return Response({'mensaje': "Ya existe una empresa con este nombre", "codigo": 13}, status=status.HTTP_400_BAD_REQUEST)
                if config('ENV') == 'dev':
                    dominio = '.localhost'
                if config('ENV') == 'test':
                    dominio = '.muupservicios.online'
                if config('ENV') == 'prod':
                    dominio = '.redofice.com'
                usuario = User.objects.get(pk=parametroUsuario)
                call_command('create_tenant', schema_name=subdominio, domain_domain=subdominio+dominio, nombre=nombre, domain_is_primary='0', imagen=imagen) 
                #call_command('tenant_command', 'loaddata', 'general/fixtures/identificacion.json', '--schema', 'demo')
                #call_command('tenant_command', 'loaddata', 'general/fixtures/identificacion.json', schema_name='demo', verbosity=0) 
                #Asi no se deben ejecutar los fixtures
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/pais.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/estado.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/ciudad.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/identificacion.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/tipo_persona.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/regimen.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/movimiento_clase.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/movimiento_tipo.json")
                
                empresa = Empresa.objects.filter(**{'schema_name':subdominio}).first()                        
                data = {'usuario': usuario.id, 'empresa': empresa.id}
                usuario_empresa_serializer = UsuarioEmpresaSerializador(data=data)            
                if usuario_empresa_serializer.is_valid():
                    usuario_empresa_serializer.save()               
                    return Response({'empresa': True}, status=status.HTTP_200_OK)            
                return Response({'mensaje':'Errores en la creacion usuario empresa', 'codigo':12, 'validaciones': usuario_empresa_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'mensaje': 'Debe suministrar un subdominio, nombre y el usuario', 'codigo':11}, status=status.HTTP_400_BAD_REQUEST)            
        except FileNotFoundError:
            return Response({'mensaje': 'Inesperado e indefinido', 'codigo':0}, status=status.HTTP_400_BAD_REQUEST)            
        except User.DoesNotExist:
            return Response({'mensaje':'No existe el usuario para crear la empresa', 'codigo':17}, status=status.HTTP_400_BAD_REQUEST)
        