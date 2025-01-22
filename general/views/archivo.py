from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from general.models.archivo import GenArchivo
from general.models.documento import GenDocumento
from general.serializers.archivo import GenArchivoSerializador
from utilidades.utilidades import Utilidades
from io import BytesIO
import base64

class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = GenArchivo.objects.all()
    serializer_class = GenArchivoSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'cargar',)
    def cargar(self, request):
        raw = request.data        
        archivo_base64 = raw.get('archivo_base64')   
        documento_id = raw.get('documento_id')     
        if archivo_base64 and documento_id:
            try:
                documento = GenDocumento.objects.get(pk=documento_id)
                try:                        
                    objeto_base64 = Utilidades.separar_base64(archivo_base64)
                    #archivo_data = base64.b64decode(archivo_base64)
                    #archivo = BytesIO(archivo_data)
                    return Response({'mensaje': f'Archivo cargado correctamente', 'base64': objeto_base64['base64_raw']}, status=status.HTTP_200_OK)                                         
                except ValueError as e:
                    return Response({'mensaje': str(e), 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                                   
            except GenDocumento.DoesNotExist:
                return Response({'mensaje':'El documento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)                        
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

     
          
      
    

