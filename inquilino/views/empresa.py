from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from inquilino.models import Empresa
from inquilino.serializers.empresa import EmpresaSerializer, EmpresaActualizarSerializador
from inquilino.serializers.usuario_empresa import UsuarioEmpresaSerializador
from seguridad.models import User
from django.core.management import call_command
from django.shortcuts import get_object_or_404
from decouple import config
from utilidades.space_do import SpaceDo
import os


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer    
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Empresa, pk=pk)

    def create(self, request):
        try:            
            subdominio = request.data.get('subdominio')
            parametroUsuario = request.data.get('usuario')
            nombre = request.data.get('nombre')
            imagen = request.data.get('imagen')
            plan_id = request.data.get('plan_id')
            if subdominio and parametroUsuario and nombre and plan_id:
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
                call_command('create_tenant', schema_name=subdominio, domain_domain=subdominio+dominio, nombre=nombre, domain_is_primary='0', imagen=f"{config('ENV')}/empresa/logo_defecto.jpg", usuario_id=usuario.id, plan_id=plan_id, usuarios=1)
                #call_command('tenant_command', 'loaddata', 'general/fixtures/identificacion.json', '--schema', 'demo')
                #call_command('tenant_command', 'loaddata', 'general/fixtures/identificacion.json', schema_name='demo', verbosity=0) 
                #Asi no se deben ejecutar los fixtures
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/pais.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/estado.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/ciudad.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/identificacion.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/tipo_persona.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/regimen.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/documento_clase.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/documento_tipo.json")
                
                empresa = Empresa.objects.filter(**{'schema_name':subdominio}).first()                        
                data = {'usuario': usuario.id, 'empresa': empresa.id, 'rol': 'propietario'}
                usuario_empresa_serializer = UsuarioEmpresaSerializador(data=data)            
                if usuario_empresa_serializer.is_valid():
                    usuario_empresa_serializer.save()               
                    return Response({'empresa': usuario_empresa_serializer.data}, status=status.HTTP_200_OK)            
                return Response({'mensaje':'Errores en la creacion usuario empresa', 'codigo':12, 'validaciones': usuario_empresa_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'mensaje': 'Debe suministrar un subdominio, plan, nombre y el usuario', 'codigo':11}, status=status.HTTP_400_BAD_REQUEST)            
        except FileNotFoundError:
            return Response({'mensaje': 'Inesperado e indefinido', 'codigo':0}, status=status.HTTP_400_BAD_REQUEST)            
        except User.DoesNotExist:
            return Response({'mensaje':'No existe el usuario para crear la empresa', 'codigo':17}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        empresa = self.get_object(pk)
        empresaSerializador = self.serializer_class(empresa)
        return Response(empresaSerializador.data)

    def update(self, request, pk=None):
        empresa = self.get_object(pk)
        empresaSerializador = EmpresaActualizarSerializador(empresa, data=request.data)
        if empresaSerializador.is_valid():
            empresaSerializador.save()
            return Response({'actualizacion': True, 'empresa': empresaSerializador.data}, status=status.HTTP_201_CREATED)            
        return Response({'mensaje':'Errores en la actualizacion', 'codigo':23, 'validaciones': empresaSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        empresa = self.get_object(pk)        
        self.perform_destroy(empresa)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path=r'consulta-subdominio',)
    def consulta_subdominio(self, request):
        try:
            subdominio = request.data.get('subdominio')
            empresa = Empresa.objects.get(schema_name=subdominio)
            serializer = EmpresaSerializer(empresa)
            return Response({'empresa':serializer.data}, status=status.HTTP_200_OK)    
        except Empresa.DoesNotExist:
            return Response({'mensaje':'No existe el registro', 'codigo':15}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=["post"], url_path=r'validar',)
    def validar(self, request):
        try:
            subdominio = request.data.get('subdominio')
            Empresa.objects.get(schema_name=subdominio)
            return Response({'validar':False}, status=status.HTTP_200_OK)    
        except Empresa.DoesNotExist:
            return Response({'validar':True}, status=status.HTTP_200_OK)        
        
    @action(detail=False, methods=["post"], url_path=r'cargar-logo',)
    def cargar_logo(self, request):
        try:
            raw = request.data
            empresa_id = raw.get('empresa_id')
            imagenB64 = raw.get('imagenB64')
            if empresa_id:
                empresa = Empresa.objects.get(pk=empresa_id)
                arrDatosB64 = imagenB64.split(",")
                base64Crudo = arrDatosB64[1]
                arrTipo = arrDatosB64[0].split(";")
                arrData = arrTipo[0].split(":")
                contentType = arrData[1]
                archivo = f"{config('ENV')}/empresa/logo_{empresa_id}.jpg"
                spaceDo = SpaceDo()
                spaceDo.putB64(archivo, base64Crudo, contentType)
                empresa.imagen = archivo
                empresa.save()
                return Response({'cargar':True, 'imagen':f"https://itrio.fra1.digitaloceanspaces.com/{archivo}"}, status=status.HTTP_200_OK)                  
            else: 
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except Empresa.DoesNotExist:
            return Response({'mensaje':'La empresa no existe', 'codigo':15}, status=status.HTTP_404_NOT_FOUND)  

    @action(detail=False, methods=["post"], url_path=r'limpiar-logo',)
    def limpiar_logo(self, request):
        try:
            raw = request.data
            empresa_id = raw.get('empresa_id')    
            if empresa_id:
                empresa = Empresa.objects.get(pk=empresa_id)                
                spaceDo = SpaceDo()
                spaceDo.eliminar(empresa.imagen)
                empresa.imagen = f"{config('ENV')}/empresa/logo_defecto.jpg"
                empresa.save()
                return Response({'limpiar':True, 'imagen':f"https://itrio.fra1.digitaloceanspaces.com/{empresa.imagen}"}, status=status.HTTP_200_OK)                  
            else: 
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except Empresa.DoesNotExist:
            return Response({'mensaje':'La empresa no existe', 'codigo':15}, status=status.HTTP_404_NOT_FOUND)               
