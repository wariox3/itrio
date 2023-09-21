from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from inquilino.models import Inquilino
from general.models.empresa import Empresa
from inquilino.serializers.inquilino import InquilinoSerializador, InquilinoActualizarSerializador
from inquilino.serializers.usuario_inquilino import UsuarioInquilinoSerializador
from general.serializers.empresa import EmpresaSerializador

from seguridad.models import User
from django.core.management import call_command
from django.shortcuts import get_object_or_404
from decouple import config
from utilidades.space_do import SpaceDo
import os


class InquilinoViewSet(viewsets.ModelViewSet):
    queryset = Inquilino.objects.all()
    serializer_class = InquilinoSerializador    
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Inquilino, pk=pk)

    def create(self, request):
        try:            
            subdominio = request.data.get('subdominio')
            usuario_id = request.data.get('usuario_id')
            plan_id = request.data.get('plan_id')
            nombre = request.data.get('nombre')                        
            numero_identificacion = request.data.get('numero_identificacion')
            direccion = request.data.get('direccion')
            telefono = request.data.get('telefono')
            correo = request.data.get('correo')
            identificacion = request.data.get('identificacion_id')
            ciudad = request.data.get('ciudad_id')
            if subdominio and usuario_id and nombre and plan_id and numero_identificacion and direccion and telefono and correo and identificacion and ciudad:
                inquilinoValidacion = Inquilino.objects.filter(**{'schema_name':subdominio})
                if inquilinoValidacion:
                    return Response({'mensaje': "Ya existe una empresa con este nombre", "codigo": 13}, status=status.HTTP_400_BAD_REQUEST)
                if config('ENV') == 'dev':
                    dominio = '.localhost'
                if config('ENV') == 'test':
                    dominio = '.muupservicios.online'
                if config('ENV') == 'prod':
                    dominio = '.redofice.com'
                usuario = User.objects.get(pk=usuario_id)
                call_command('create_tenant', schema_name=subdominio, domain_domain=subdominio+dominio, nombre=nombre, domain_is_primary='0', imagen=f"{config('ENV')}/empresa/logo_defecto.jpg", usuario_id=usuario.id, plan_id=plan_id, usuarios=1)
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/pais.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/estado.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/ciudad.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/identificacion.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/tipo_persona.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/regimen.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/documento_clase.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/documento_tipo.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/forma_pago.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/metodo_pago.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/impuesto.json")
                
                inquilino = Inquilino.objects.filter(**{'schema_name':subdominio}).first()                        
                data = {'usuario': usuario.id, 'inquilino': inquilino.id, 'rol': 'propietario'}
                usuarioInquilinoSerializador = UsuarioInquilinoSerializador(data=data)            
                if usuarioInquilinoSerializador.is_valid():
                    usuarioInquilinoSerializador.save()
                    return Response({'empresa': usuarioInquilinoSerializador.data}, status=status.HTTP_200_OK)            
                return Response({'mensaje':'Errores en la creacion del inquilino', 'codigo':12, 'validaciones': usuarioInquilinoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'mensaje': 'Faltan datos para el consumo de la api', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                   
        except User.DoesNotExist:
            return Response({'mensaje':'No existe el usuario para crear la empresa', 'codigo':17}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        empresa = self.get_object(pk)
        empresaSerializador = self.serializer_class(empresa)
        return Response(empresaSerializador.data)

    def update(self, request, pk=None):
        empresa = self.get_object(pk)
        empresaSerializador = InquilinoActualizarSerializador(empresa, data=request.data)
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
            empresa = Inquilino.objects.get(schema_name=subdominio)
            serializer = InquilinoSerializador(empresa)
            return Response({'empresa':serializer.data}, status=status.HTTP_200_OK)    
        except Inquilino.DoesNotExist:
            return Response({'mensaje':'No existe el registro', 'codigo':15}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=["post"], url_path=r'validar',)
    def validar(self, request):
        try:
            subdominio = request.data.get('subdominio')
            Inquilino.objects.get(schema_name=subdominio)
            return Response({'validar':False}, status=status.HTTP_200_OK)    
        except Inquilino.DoesNotExist:
            return Response({'validar':True}, status=status.HTTP_200_OK)        
        
    @action(detail=False, methods=["post"], url_path=r'cargar-logo',)
    def cargar_logo(self, request):
        try:
            raw = request.data
            empresa_id = raw.get('empresa_id')
            imagenB64 = raw.get('imagenB64')
            if empresa_id:
                empresa = Inquilino.objects.get(pk=empresa_id)
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
        except Inquilino.DoesNotExist:
            return Response({'mensaje':'La empresa no existe', 'codigo':15}, status=status.HTTP_404_NOT_FOUND)  

    @action(detail=False, methods=["post"], url_path=r'limpiar-logo',)
    def limpiar_logo(self, request):
        try:
            raw = request.data
            empresa_id = raw.get('empresa_id')    
            if empresa_id:
                empresa = Inquilino.objects.get(pk=empresa_id)                
                spaceDo = SpaceDo()
                spaceDo.eliminar(empresa.imagen)
                empresa.imagen = f"{config('ENV')}/empresa/logo_defecto.jpg"
                empresa.save()
                return Response({'limpiar':True, 'imagen':f"https://itrio.fra1.digitaloceanspaces.com/{empresa.imagen}"}, status=status.HTTP_200_OK)                  
            else: 
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except Inquilino.DoesNotExist:
            return Response({'mensaje':'La empresa no existe', 'codigo':15}, status=status.HTTP_404_NOT_FOUND)               
