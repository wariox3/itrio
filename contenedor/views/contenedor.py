from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from contenedor.models import Contenedor
from general.models.empresa import Empresa
from contenedor.serializers.contenedor import ContenedorSerializador, ContenedorActualizarSerializador
from contenedor.serializers.usuario_contenedor import UsuarioContenedorSerializador
from general.serializers.empresa import EmpresaSerializador
from seguridad.models import User
from django.core.management import call_command
from django.shortcuts import get_object_or_404
from decouple import config
from utilidades.space_do import SpaceDo
from django_tenants.utils import schema_context
import os


class ContenedorViewSet(viewsets.ModelViewSet):
    queryset = Contenedor.objects.all()
    serializer_class = ContenedorSerializador    
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Contenedor, pk=pk)

    def create(self, request):
        try:            
            subdominio = request.data.get('subdominio')
            usuario_id = request.data.get('usuario_id')
            plan_id = request.data.get('plan_id')
            nombre = request.data.get('nombre')  
            identificacion = request.data.get('identificacion_id')
            numero_identificacion = request.data.get('numero_identificacion')
            digito_verificacion = request.data.get('digito_verificacion')
            direccion = request.data.get('direccion')
            telefono = request.data.get('telefono')
            correo = request.data.get('correo')
            ciudad = request.data.get('ciudad_id')
            if subdominio and usuario_id and nombre and plan_id and identificacion and numero_identificacion and digito_verificacion and direccion and telefono and correo and ciudad:
                contenedorValidacion = Contenedor.objects.filter(**{'schema_name':subdominio})
                if contenedorValidacion:
                    return Response({'mensaje': "Ya existe una empresa con este nombre", "codigo": 13}, status=status.HTTP_400_BAD_REQUEST)
                dominio = '.' + config('DOMINIO_BACKEND')
                usuario = User.objects.get(pk=usuario_id)
                imagenReferencia = f"{config('ENV')}/empresa/logo_defecto.jpg"
                call_command('create_tenant', schema_name=subdominio, domain_domain=subdominio+dominio, nombre=nombre, domain_is_primary='0', imagen=imagenReferencia, usuario_id=usuario.id, plan_id=plan_id, usuarios=1)
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
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/plazo_pago.json")
                os.system(f"python3 manage.py tenant_command loaddata --schema={subdominio} general/fixtures/impuesto.json")            

                contenedor = Contenedor.objects.filter(**{'schema_name':subdominio}).first()                        
                data = {'usuario': usuario.id, 'contenedor': contenedor.id, 'rol': 'propietario'}
                usuarioContenedorSerializador = UsuarioContenedorSerializador(data=data)            
                if usuarioContenedorSerializador.is_valid():
                    usuarioContenedorSerializador.save()
                    with schema_context(subdominio):
                        data = {
                            'id':1,
                            'identificacion': identificacion,                            
                            'numero_identificacion': numero_identificacion,
                            'digito_verificacion': digito_verificacion,
                            'nombre_corto': nombre,
                            'direccion': direccion,
                            'telefono': telefono,
                            'correo': correo,
                            'ciudad': ciudad,
                            'imagen': imagenReferencia,
                            'tipo_persona': 1,                            
                            'regimen':1,
                            'contenedor_id':contenedor.id}
                        empresaSerializador = EmpresaSerializador(data=data)                        
                        if empresaSerializador.is_valid():
                            empresaSerializador.save()
                            return Response({'contenedor': usuarioContenedorSerializador.data}, status=status.HTTP_200_OK)            
                        return Response({'mensaje':'Errores en la creacion de la empresa', 'codigo':12, 'validaciones': empresaSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)        
                return Response({'mensaje':'Errores en la creacion del contenedor', 'codigo':12, 'validaciones': usuarioContenedorSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'mensaje': 'Faltan datos para el consumo de la api', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                   
        except User.DoesNotExist:
            return Response({'mensaje':'No existe el usuario para crear la empresa', 'codigo':17}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        empresa = self.get_object(pk)
        empresaSerializador = self.serializer_class(empresa)
        return Response(empresaSerializador.data)

    def update(self, request, pk=None):
        empresa = self.get_object(pk)
        empresaSerializador = ContenedorActualizarSerializador(empresa, data=request.data)
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
            empresa = Contenedor.objects.get(schema_name=subdominio)
            serializer = ContenedorSerializador(empresa)
            return Response({'empresa':serializer.data}, status=status.HTTP_200_OK)    
        except Contenedor.DoesNotExist:
            return Response({'mensaje':'No existe el registro', 'codigo':15}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=["post"], url_path=r'validar',)
    def validar(self, request):
        try:
            subdominio = request.data.get('subdominio')
            Contenedor.objects.get(schema_name=subdominio)
            return Response({'validar':False}, status=status.HTTP_200_OK)    
        except Contenedor.DoesNotExist:
            return Response({'validar':True}, status=status.HTTP_200_OK)        
        
    @action(detail=False, methods=["post"], url_path=r'cargar-logo',)
    def cargar_logo(self, request):
        try:
            raw = request.data
            empresa_id = raw.get('empresa_id')
            imagenB64 = raw.get('imagenB64')
            if empresa_id:
                empresa = Contenedor.objects.get(pk=empresa_id)
                arrDatosB64 = imagenB64.split(",")
                base64Crudo = arrDatosB64[1]
                arrTipo = arrDatosB64[0].split(";")
                arrData = arrTipo[0].split(":")
                contentType = arrData[1]
                archivo = f"{config('ENV')}/contenedor/logo_{empresa_id}.jpg"
                spaceDo = SpaceDo()
                spaceDo.putB64(archivo, base64Crudo, contentType)
                empresa.imagen = archivo
                empresa.save()
                return Response({'cargar':True, 'imagen':f"https://itrio.fra1.digitaloceanspaces.com/{archivo}"}, status=status.HTTP_200_OK)                  
            else: 
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except Contenedor.DoesNotExist:
            return Response({'mensaje':'La empresa no existe', 'codigo':15}, status=status.HTTP_404_NOT_FOUND)  

    @action(detail=False, methods=["post"], url_path=r'limpiar-logo',)
    def limpiar_logo(self, request):
        try:
            raw = request.data
            empresa_id = raw.get('empresa_id')    
            if empresa_id:
                empresa = Contenedor.objects.get(pk=empresa_id)                
                spaceDo = SpaceDo()
                spaceDo.eliminar(empresa.imagen)
                empresa.imagen = f"{config('ENV')}/contenedor/logo_defecto.jpg"
                empresa.save()
                return Response({'limpiar':True, 'imagen':f"https://itrio.fra1.digitaloceanspaces.com/{empresa.imagen}"}, status=status.HTTP_200_OK)                  
            else: 
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except Contenedor.DoesNotExist:
            return Response({'mensaje':'La empresa no existe', 'codigo':15}, status=status.HTTP_404_NOT_FOUND)               
