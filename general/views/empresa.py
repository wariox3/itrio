from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from general.models.empresa import Empresa
from general.serializers.empresa import EmpresaSerializador, EmpresaActualizarSerializador
from rest_framework.decorators import action
from decouple import config
from utilidades.space_do import SpaceDo
from utilidades.wolframio import consumirPost


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializador    
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):        
        if Empresa.objects.filter(pk=1).exists():
            return Response({'mensaje':'Ya se creó la empresa', 'codigo':14}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = request.data
            empresaSerializador = EmpresaSerializador(data=request.data)
            if empresaSerializador.is_valid():
                empresaSerializador.save()                         
                return Response({'empresa': empresaSerializador.data}, status=status.HTTP_200_OK)
            return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': empresaSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None):
        empresa = self.get_object()
        empresaSerializador = EmpresaActualizarSerializador(empresa, data=request.data)
        if empresaSerializador.is_valid():
            empresaSerializador.save()
            return Response({'actualizacion': True, 'empresa': empresaSerializador.data}, status=status.HTTP_201_CREATED)            
        return Response({'mensaje':'Errores en la actualizacion', 'codigo':23, 'validaciones': empresaSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
    
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
                archivo = f"{config('ENV')}/empresa/logo_{empresa.contenedor_id}_{empresa_id}.jpg"
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

    @action(detail=False, methods=["post"], url_path=r'activar',)
    def activar_cuenta_wolframio(self, request):
        try:
            raw = request.data
            empresa_id = raw.get('empresa_id')
            if empresa_id:
                empresa = Empresa.objects.get(pk=empresa_id)
                datos = ""
                url = "/api/cuenta/nuevo"
                datos = {
                    "numeroIdentificacion" : empresa.numero_identificacion,
                    "nombre" : empresa.nombre_corto,
                    "celular" : empresa.telefono,
                    "correo" : empresa.correo,
                    "ciudadId" : empresa.ciudad.id,
                    "identificacionId" : empresa.identificacion.id,
                    "webhookEmision" : raw.get('webhookEmision'),
                    "webhookNotificacion" : raw.get('webhookNotificacion'),
                    "setPruebas" : raw.get('setPruebas')
                }

                respuesta = consumirPost(datos, url)
                
                if 'id' in respuesta:
                    rededoc_id = respuesta.get('id')
                    if empresa.rededoc_id is None or empresa.rededoc_id == '':
                        empresa.rededoc_id = rededoc_id
                        empresa.save()
                    else:
                        return Response({'mensaje': 'La empresa ya se encuentra activa', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    validacion = respuesta.get('validacion')
                    return Response({'mensaje': {validacion}, 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)
                
                return Response({'validar':True}, status=status.HTTP_200_OK)        
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

        except Empresa.DoesNotExist:
            return Response({'mensaje': 'La empresa no existe', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)