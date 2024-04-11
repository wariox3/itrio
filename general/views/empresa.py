from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from general.models.empresa import Empresa
from general.serializers.empresa import EmpresaSerializador, EmpresaActualizarSerializador
from rest_framework.decorators import action
from decouple import config
from utilidades.space_do import SpaceDo
from utilidades.wolframio import Wolframio

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
                archivo = f"itrio/{config('ENV')}/empresa/logo_{empresa.contenedor_id}_{empresa_id}.jpg"
                spaceDo = SpaceDo()
                spaceDo.putB64(archivo, base64Crudo, contentType)
                empresa.imagen = archivo
                empresa.save()
                return Response({'cargar':True, 'imagen':f"https://{config('DO_BUCKET')}.{config('DO_REGION')}.digitaloceanspaces.com/{archivo}"}, status=status.HTTP_200_OK)                  
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
                empresa.imagen = f"itrio/{config('ENV')}/empresa/logo_defecto.jpg"
                empresa.save()
                return Response({'limpiar':True, 'imagen':f"https://{config('DO_BUCKET')}.{config('DO_REGION')}.digitaloceanspaces.com/{empresa.imagen}"}, status=status.HTTP_200_OK)                  
            else: 
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except Empresa.DoesNotExist:
            return Response({'mensaje':'La empresa no existe', 'codigo':15}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"], url_path=r'activar',)
    def activar_cuenta_wolframio(self, request):
        try:
            raw = request.data
            empresa_id = raw.get('empresa_id')
            resolucion_id = raw.get('resolucion_id')
            set_pruebas = raw.get('set_pruebas')
            if empresa_id and resolucion_id and set_pruebas:                                            
                wolframio = Wolframio()
                respuesta = wolframio.activarCuenta(set_pruebas, resolucion_id)
                if respuesta['error'] == False:
                    return Response({'validar':True}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':respuesta['mensaje'], 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje':'Faltan parametros, no tiene una resolución seleccionada', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except Empresa.DoesNotExist:
            return Response({'mensaje': 'La empresa no existe', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)